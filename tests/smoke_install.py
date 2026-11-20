"""Verify local builds and smoke-test their installed environments."""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import math
import subprocess
import sys
import tarfile
import zipfile
from copy import deepcopy
from numbers import Real
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    import gymnasium as gym
    from gymnasium.envs.mujoco import MujocoEnv
    from safety_gymnasium2.tasks.safe_multi_agent.tasks.velocity.safe_mujoco_multi import SafeMAEnv
    from safety_gymnasium2.utils._types import NativeStep

_ARCHIVE_LIMIT = 100_000_000
_LICENSE_FILES = frozenset({'LICENSE', 'LICENSE-MIT', 'NOTICE'})
_CORE_MESHES = frozenset(
    PurePosixPath('safety_gymnasium2/assets/meshes', filename)
    for filename in (
        'chassis_differential.STL',
        'left_front_wheel.obj',
        'left_rear_wheel.obj',
        'left_steering_hinge.STL',
        'right_front_wheel.obj',
        'right_rear_wheel.obj',
        'right_steering_hinge.STL',
    )
)
_REMOVED_ARCHIVE_PARTS = frozenset(
    {
        'asset_packs',
        'legacy',
        'safe_isaac_gym',
        'safe_vla',
        'building_button',
        'building_goal',
        'building_push',
        'formula_one',
        'race',
        'building_button.yaml',
        'building_goal.yaml',
        'building_push.yaml',
        'formula_one.yaml',
        'race.yaml',
    }
)


def check_archives(directory: Path) -> None:
    """Inspect the core wheel and source archive for the release."""
    for suffix in ('.whl', '.tar.gz'):
        paths = list(directory.glob(f'*{suffix}'))
        assert len(paths) == 1, f'Expected one core {suffix}, found {paths}'
        path = paths[0]
        assert path.name.startswith('safety_gymnasium2-'), path.name
        size = path.stat().st_size
        assert size < _ARCHIVE_LIMIT, f'{path.name} is {size} bytes'
        if suffix == '.whl':
            with zipfile.ZipFile(path) as archive:
                members = [
                    PurePosixPath(item.filename) for item in archive.infolist() if not item.is_dir()
                ]
            licenses = {
                item.name
                for item in members
                if len(item.parts) == 3
                and item.parts[0].endswith('.dist-info')
                and item.parts[1] == 'licenses'
            }
        else:
            with tarfile.open(path) as archive:
                members = [
                    PurePosixPath(*PurePosixPath(item.name).parts[1:])
                    for item in archive.getmembers()
                    if item.isfile()
                ]
            licenses = {item.name for item in members if len(item.parts) == 1}
        assert licenses >= _LICENSE_FILES, f'{path.name} missing {_LICENSE_FILES - licenses}'
        for member in members:
            assert _REMOVED_ARCHIVE_PARTS.isdisjoint(member.parts), member
        meshes = {member for member in members if 'meshes' in member.parts}
        assert meshes == _CORE_MESHES, f'{path.name} unexpected mesh inventory {meshes}'
        textures = {member for member in members if 'textures' in member.parts}
        assert not textures, f'{path.name} unexpectedly contains textures {textures}'
        print(f'{path.name}: {size:,} bytes')


def _smoke_half_cheetah() -> None:
    import safety_gymnasium2 as sg2

    model_path = Path(sg2.__file__).resolve().parent / 'assets/xmls/half_cheetah.xml'
    for version in (0, 1, 2):
        with sg2.make(f'SafetyHalfCheetahVelocity-v{version}') as env:
            _check_half_cheetah_model(cast('MujocoEnv', env.unwrapped), model_path)
            env.reset(seed=17)
            assert len(env.step(env.action_space.sample())) == 6
    for partition in ('6x1', '2x3'):
        env = sg2.make_ma('HalfCheetah', partition)
        try:
            _check_half_cheetah_model(
                cast('MujocoEnv', env.env.single_agent_env.unwrapped), model_path
            )
            env.reset(seed=17)
            action_by_agent = {agent: env.action_space(agent).sample() for agent in env.agents}
            assert len(env.step(action_by_agent)) == 6
        finally:
            env.close()


def _check_half_cheetah_model(env: MujocoEnv, model_path: Path) -> None:
    assert Path(env.fullpath).resolve() == model_path
    assert math.isclose(float(env.model.body_mass.sum()), 14.0)


def _base_task_kwargs(env_id: str) -> dict[str, Any]:
    from safety_gymnasium2.tasks.safe_navigation.button.button_configs import button_level0
    from safety_gymnasium2.tasks.safe_navigation.circle.circle_configs import circle_level0
    from safety_gymnasium2.tasks.safe_navigation.goal.goal_configs import goal_level0
    from safety_gymnasium2.tasks.safe_navigation.push.push_configs import push_level0
    from safety_gymnasium2.tasks.safe_navigation.run.run_configs import run_level0

    for task, config in (
        ('ButtonBase', button_level0),
        ('CircleBase', circle_level0),
        ('GoalBase', goal_level0),
        ('PushBase', push_level0),
        ('RunBase', run_level0),
    ):
        if task in env_id:
            # The registry smoke supplies the horizon through the environment factory.
            config_by_name = deepcopy(config)
            config_by_name.pop('num_steps', None)
            return {'config': config_by_name}
    return {}


def _smoke_catalog() -> None:
    import gymnasium as gym
    import safety_gymnasium2 as sg2
    from safety_gymnasium2.tasks.safe_multi_agent.builder import Builder as MultiAgentBuilder
    from safety_gymnasium2.utils.registration import safe_registry

    for env_id in sorted(safe_registry):
        with sg2.make(env_id, max_episode_steps=1, **_base_task_kwargs(env_id)) as env:
            if isinstance(env.unwrapped, MultiAgentBuilder):
                _smoke_multi_agent_step(env, env_id)
            else:
                _smoke_single_agent_step(env, env_id, gymnasium_api=False)

    alias_ids = sorted(env_id for env_id in gym.registry if env_id.startswith('SafetyGymnasium2/'))
    assert alias_ids, 'The Gymnasium alias registry is empty'
    for env_id in alias_ids:
        with gym.make(env_id, max_episode_steps=1, **_base_task_kwargs(env_id)) as env:
            _smoke_single_agent_step(env, env_id, gymnasium_api=True)

    for scenario, partition in (
        ('Ant', '2x4'),
        ('Ant', '4x2'),
        ('HalfCheetah', '6x1'),
        ('HalfCheetah', '2x3'),
        ('Hopper', '3x1'),
        ('Humanoid', '9|8'),
        ('Swimmer', '2x1'),
        ('Walker2d', '2x3'),
    ):
        multi_env = sg2.make_ma(scenario, partition, max_episode_steps=1)
        try:
            _smoke_multi_agent_step(multi_env, f'{scenario} {partition}')
        finally:
            multi_env.close()

    print(f'Smoked {len(safe_registry)} native environments, {len(alias_ids)} aliases, and make_ma')


def _smoke_single_agent_step(env: gym.Env, env_id: str, *, gymnasium_api: bool) -> None:
    observation, _ = env.reset(seed=17)
    assert env.observation_space.contains(observation), env_id
    env.action_space.seed(17)
    action = env.action_space.sample()
    if gymnasium_api:
        observation, reward, _, truncated, info = env.step(action)
        cost = info['cost']
    else:
        observation, reward, cost, _, truncated, _ = cast('NativeStep', env.step(action))
    assert env.observation_space.contains(observation), env_id
    assert isinstance(reward, Real) and isinstance(cost, Real) and truncated, env_id


def _smoke_multi_agent_step(env: gym.Env | SafeMAEnv, env_id: str) -> None:
    from gymnasium import Env

    observation_by_agent, _ = env.reset(seed=17)
    if isinstance(env, Env):
        action_space = env.get_wrapper_attr('action_space')
        observation_space = env.get_wrapper_attr('observation_space')
    else:
        action_space = env.action_space
        observation_space = env.observation_space

    assert observation_by_agent, env_id
    actions_by_agent = {}
    for agent, observation in observation_by_agent.items():
        assert observation_space(agent).contains(observation), (env_id, agent)
        space = action_space(agent)
        space.seed(17)
        actions_by_agent[agent] = space.sample()

    _, rewards_by_agent, costs_by_agent, _, truncation_by_agent, _ = cast(
        'NativeStep', env.step(actions_by_agent)
    )
    assert actions_by_agent.keys() == rewards_by_agent.keys() == costs_by_agent.keys(), env_id
    assert all(truncation_by_agent.values()), env_id


def _smoke_rendering() -> None:
    import numpy as np
    import safety_gymnasium2 as sg2

    for env_id, mode, shape in (
        ('SafetyPointGoal0-v0', 'rgb_array', (32, 48, 3)),
        ('SafetyRacecarPush0-v0', 'depth_array', (32, 48)),
    ):
        with sg2.make(
            env_id,
            config={'observation_flatten': False},
            render_mode=mode,
            width=48,
            height=32,
            max_episode_steps=1,
        ) as env:
            _smoke_single_agent_step(env, env_id, gymnasium_api=False)
            assert np.shape(env.render()) == shape, env_id


def smoke_install() -> None:
    """Exercise the core catalog and rendering in an isolated installation."""
    import safety_gymnasium2 as sg2

    metadata = importlib.metadata.metadata('safety-gymnasium2')
    assert sg2.__version__ == metadata['Version']
    assert metadata['License-Expression'] == 'Apache-2.0 AND MIT'
    assert set(metadata.get_all('License-File') or ()) >= _LICENSE_FILES
    assert not metadata.get_all('Provides-Extra'), 'Core unexpectedly provides extras'
    assert Path(sg2.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    assert importlib.util.find_spec('safety_gymnasium2.tasks.safe_isaac_gym') is None
    assert importlib.util.find_spec('safety_gymnasium2.tasks.safe_vla') is None

    _smoke_catalog()
    _smoke_rendering()
    half_cheetah = subprocess.run(
        [sys.executable, '-I', __file__, 'half-cheetah'],
        capture_output=True,
        text=True,
        check=False,
    )
    output = half_cheetah.stdout + half_cheetah.stderr
    assert half_cheetah.returncode == 0, output
    assert 'settotalmass' not in output.lower(), output
    print('Core install smoke passed')


def main() -> None:
    """Run archive validation or smoke tests for an installed package."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('archives', 'core', 'half-cheetah'))
    parser.add_argument('--dist', type=Path, default=Path('dist'))
    args = parser.parse_args()
    if args.mode == 'archives':
        check_archives(args.dist)
    elif args.mode == 'half-cheetah':
        _smoke_half_cheetah()
    else:
        smoke_install()


if __name__ == '__main__':
    main()
