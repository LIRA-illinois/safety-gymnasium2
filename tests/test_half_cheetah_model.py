"""HalfCheetah model compatibility and benchmark parity regressions."""

from __future__ import annotations

import subprocess
import sys
from importlib.resources import files
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast
from xml.etree import ElementTree

import gymnasium as gym
import numpy as np
import safety_gymnasium2 as sg2
from absl.testing import absltest, parameterized
from gymnasium.envs.mujoco import MujocoEnv, half_cheetah_v4
from gymnasium_robotics.envs.multiagent_mujoco import mujoco_multi
from mujoco import MjData, MjModel  # ty: ignore[missing-module-member]

_MODEL_NAME = 'half_cheetah.xml'
_BUNDLED_MODEL = Path(__file__).resolve().parents[1] / 'safety_gymnasium2/assets/xmls' / _MODEL_NAME
_HORIZON = 200


def _upstream_model() -> ElementTree.Element:
    asset = files('gymnasium.envs.mujoco').joinpath('assets', _MODEL_NAME)
    return ElementTree.fromstring(asset.read_text(encoding='utf-8'))


def _assert_model_matches(actual: MujocoEnv, reference: MjModel, xml_file: Path) -> None:
    np.testing.assert_equal(Path(actual.fullpath).resolve(), xml_file)
    np.testing.assert_equal(actual.model.body_mass, reference.body_mass)
    np.testing.assert_equal(actual.model.body_inertia, reference.body_inertia)
    np.testing.assert_equal(actual.model.stat.meanmass, reference.stat.meanmass)


def _start_running(*envs: MujocoEnv) -> None:
    for env in envs:
        velocity = env.data.qvel.copy()
        velocity[0] = 5.0
        env.set_state(env.data.qpos.copy(), velocity)


class _LegacyHalfCheetahV4(half_cheetah_v4.HalfCheetahEnv):
    """Gymnasium's v4 environment using the explicit legacy reference asset."""

    def __init__(self, xml_file: str) -> None:
        self._legacy_xml_file = xml_file
        super().__init__()

    def _initialize_simulation(self) -> tuple[MjModel, MjData]:
        self.fullpath = self._legacy_xml_file
        return super()._initialize_simulation()


class HalfCheetahModelTest(parameterized.TestCase):
    def _write_model(self, kind: str) -> str:
        xml = _upstream_model()
        compiler = xml.find('compiler')
        default_geom = xml.find('default/geom')
        assert compiler is not None and default_geom is not None
        if kind == 'legacy':
            # Reconstruct the compiler scaling after Gymnasium adopts its density replacement.
            compiler.set('settotalmass', '14')
            default_geom.attrib.pop('density', None)
        else:
            compiler.attrib.pop('settotalmass', None)
            default_geom.set('density', '850')
        directory = self.enter_context(TemporaryDirectory())
        path = Path(directory, f'{kind}.xml')
        ElementTree.ElementTree(xml).write(path, encoding='utf-8')
        return str(path)

    def _legacy_xml_file(self) -> str:
        path = self._write_model('legacy')
        try:
            MjModel.from_xml_path(path)
        except ValueError as error:
            if 'settotalmass' not in str(error):
                raise
            self.skipTest('This MuJoCo version no longer compiles the legacy compiler attribute.')
        return path

    @parameterized.named_parameters(('v0', 0, 2.8795), ('v1', 1, 3.2096), ('v2', 2, 3.2096))
    def test_single_agent_matches_legacy(self, version: int, threshold: float) -> None:
        xml_file = self._legacy_xml_file()
        reference = (
            gym.make('HalfCheetah-v5', xml_file=xml_file, max_episode_steps=_HORIZON)
            if version == 2
            else gym.wrappers.TimeLimit(_LegacyHalfCheetahV4(xml_file), _HORIZON)
        )
        self.addCleanup(reference.close)
        actual = sg2.make(f'SafetyHalfCheetahVelocity-v{version}', max_episode_steps=_HORIZON)
        self.addCleanup(actual.close)
        actual_physics = cast('MujocoEnv', actual.unwrapped)
        reference_physics = cast('MujocoEnv', reference.unwrapped)
        _assert_model_matches(actual_physics, reference_physics.model, _BUNDLED_MODEL)
        np.testing.assert_equal(actual.reset(seed=76)[0], reference.reset(seed=76)[0])
        _start_running(actual_physics, reference_physics)

        actions = np.random.default_rng(87).uniform(-1, 1, (_HORIZON, 6)).astype(np.float32)
        for action in actions:
            observation, reward, terminated, truncated, info = reference.step(action)
            cost = float(info['x_velocity'] > threshold)
            np.testing.assert_equal(
                actual.step(action)[:5], (observation, reward, cost, terminated, truncated)
            )

    @parameterized.named_parameters(('6x1', '6x1', 2.932), ('2x3', '2x3', 3.227))
    def test_multi_agent_matches_legacy(self, partition: str, threshold: float) -> None:
        reference = mujoco_multi.MultiAgentMujocoEnv(
            'HalfCheetah', partition, xml_file=self._legacy_xml_file(), max_episode_steps=_HORIZON
        )
        self.addCleanup(reference.close)
        actual = sg2.make_ma('HalfCheetah', partition, max_episode_steps=_HORIZON)
        self.addCleanup(actual.close)
        actual_physics = cast('MujocoEnv', actual.env.single_agent_env.unwrapped)
        reference_physics = cast('MujocoEnv', reference.single_agent_env.unwrapped)
        _assert_model_matches(actual_physics, reference_physics.model, _BUNDLED_MODEL)
        np.testing.assert_equal(actual.reset(seed=76)[0], reference.reset(seed=76)[0])
        _start_running(actual_physics, reference_physics)

        rng = np.random.default_rng(87)
        for _ in range(_HORIZON):
            actions_by_agent = {
                agent: rng.uniform(-1, 1, reference.action_space(agent).shape).astype(np.float32)
                for agent in reference.possible_agents
            }
            (
                obs_by_agent,
                reward_by_agent,
                terminated_by_agent,
                truncated_by_agent,
                info_by_agent,
            ) = reference.step(actions_by_agent)
            agent_info = cast('dict[str, dict[str, float]]', info_by_agent)
            velocity = abs(agent_info[reference.possible_agents[0]]['x_velocity'])
            costs_by_agent = dict.fromkeys(reference.possible_agents, float(velocity > threshold))
            np.testing.assert_equal(
                actual.step(actions_by_agent)[:5],
                (
                    obs_by_agent,
                    reward_by_agent,
                    costs_by_agent,
                    terminated_by_agent,
                    truncated_by_agent,
                ),
            )

    @parameterized.parameters('single', 'multi_xml', 'multi_injected')
    def test_custom_model_retains_its_mass(self, source: str) -> None:
        xml_file = self._write_model('custom')
        reference = MjModel.from_xml_path(xml_file)
        if source == 'single':
            env = sg2.make('SafetyHalfCheetahVelocity-v2', xml_file=xml_file)
            physics = cast('MujocoEnv', env.unwrapped)
        elif source == 'multi_xml':
            env = sg2.make_ma('HalfCheetah', '6x1', xml_file=xml_file)
            physics = cast('MujocoEnv', env.env.single_agent_env.unwrapped)
        else:
            injected = gym.make('HalfCheetah-v5', xml_file=xml_file)
            self.addCleanup(injected.close)
            env = sg2.make_ma('HalfCheetah', '2x3', gym_env=injected)
            physics = cast('MujocoEnv', env.env.single_agent_env.unwrapped)
        self.addCleanup(env.close)
        _assert_model_matches(physics, reference, Path(xml_file).resolve())

    def test_default_models_compile_without_warning(self) -> None:
        command = [
            sys.executable,
            str(Path(__file__).with_name('smoke_install.py')),
            'half-cheetah',
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('settotalmass', result.stderr.lower())


if __name__ == '__main__':
    absltest.main()
