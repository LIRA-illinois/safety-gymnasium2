"""Regressions for the documented velocity cost and fixed-action replay."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, cast
from unittest import mock

import numpy as np
import safety_gymnasium2 as sg2
from absl.testing import absltest, parameterized
from gymnasium import spaces
from gymnasium.envs.mujoco import (
    MujocoEnv,
    ant_v5,
    half_cheetah_v5,
    hopper_v5,
    humanoid_v5,
    swimmer_v5,
    walker2d_v5,
)
from numpy.typing import NDArray

if TYPE_CHECKING:
    from safety_gymnasium2.utils._types import NativeStep


def _move_laterally(env: MujocoEnv, _action: NDArray, _frame_skip: int) -> None:
    env.data.qpos[1] += env.dt


class VelocityCostTest(parameterized.TestCase):
    @parameterized.named_parameters(
        ('ant', 'Ant', ant_v5.AntEnv, 2.6222, True),
        ('half_cheetah', 'HalfCheetah', half_cheetah_v5.HalfCheetahEnv, 3.2096, False),
        ('hopper', 'Hopper', hopper_v5.HopperEnv, 0.7402, False),
        ('humanoid', 'Humanoid', humanoid_v5.HumanoidEnv, 1.4149, True),
        ('swimmer', 'Swimmer', swimmer_v5.SwimmerEnv, 0.2282, False),
        ('walker', 'Walker2d', walker2d_v5.Walker2dEnv, 2.3415, False),
    )
    def test_v2_velocity_rule(
        self,
        robot: str,
        upstream: type[MujocoEnv],
        threshold: float,
        planar: bool,
    ) -> None:
        env = sg2.make(f'Safety{robot}Velocity-v2')
        self.addCleanup(env.close)
        observation, _ = env.reset(seed=12)
        action_space = cast('spaces.Box', env.action_space)
        action = np.zeros(action_space.shape, dtype=action_space.dtype)
        cases = (
            ('at threshold', threshold, 0.0, 0.0),
            ('above threshold', threshold + 1.0, 0.0, 1.0),
            ('negative forward', -threshold - 1.0, 0.0, float(planar)),
            ('lateral', 0.0, threshold + 1.0, float(planar)),
        )
        for label, x_velocity, y_velocity, expected_cost in cases:
            with (
                self.subTest(velocity=label),
                mock.patch.object(
                    upstream,
                    'step',
                    autospec=True,
                    spec_set=True,
                    return_value=(
                        observation,
                        0.0,
                        False,
                        False,
                        {'x_velocity': x_velocity, 'y_velocity': y_velocity},
                    ),
                ),
            ):
                _, _, cost, _, _, _ = cast('NativeStep', env.step(action))
                self.assertEqual(cost, expected_cost)

    @parameterized.named_parameters(('v0_planar', 'v0', 1.0), ('v1_forward', 'v1', 0.0))
    def test_swimmer_lateral_cost_changes_by_version(
        self,
        version: str,
        expected_cost: float,
    ) -> None:
        env = sg2.make(f'SafetySwimmerVelocity-{version}')
        self.addCleanup(env.close)
        env.reset(seed=12)
        native_env = cast('MujocoEnv', env.unwrapped)
        simulation = partial(_move_laterally, native_env)
        action_space = cast('spaces.Box', env.action_space)
        action = np.zeros(action_space.shape, dtype=action_space.dtype)
        with mock.patch.object(
            native_env,
            'do_simulation',
            autospec=True,
            spec_set=True,
            side_effect=simulation,
        ):
            _, _, cost, _, _, _ = cast('NativeStep', env.step(action))
        self.assertEqual(cost, expected_cost)


class ReplayTest(absltest.TestCase):
    def test_fixed_action_replay(self) -> None:
        observation_trace, signals = self._rollout()
        replay_observations, replay_signals = self._rollout()
        np.testing.assert_array_equal(observation_trace, replay_observations)
        self.assertEqual(signals, replay_signals)
        self.assertEqual(signals[-1][2:], (False, True))

    def _rollout(self) -> tuple[NDArray[np.float64], list[tuple[float, float, bool, bool]]]:
        env = sg2.make('SafetyPointGoal0-v0', max_episode_steps=3)
        self.addCleanup(env.close)
        observation, _ = env.reset(seed=42)
        observations = [observation]
        signals = []
        for action in np.array([[0.15, -0.2], [-0.2, 0.1], [0.05, 0.25]]):
            observation, reward, cost, terminated, truncated, _ = cast(
                'NativeStep', env.step(action)
            )
            observations.append(observation)
            signals.append((reward, cost, terminated, truncated))
        return np.stack(observations), signals


if __name__ == '__main__':
    absltest.main()
