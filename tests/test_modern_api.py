# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from __future__ import annotations

from functools import partial
from typing import Any, cast

import gymnasium
import numpy as np
import safety_gymnasium2 as sg2
from absl.testing import absltest, parameterized
from safety_gymnasium2.utils._types import NativeStep
from safety_gymnasium2.vector import SafetyAsyncVectorEnv, SafetySyncVectorEnv


class CostEnv(gymnasium.Env):
    """Deterministic environment with observable terminal costs."""

    observation_space = gymnasium.spaces.Discrete(5)
    action_space = gymnasium.spaces.Discrete(2)

    def __init__(self, horizon: int) -> None:
        self._horizon = horizon
        self._elapsed = 0

    def reset(self, *, seed: int | None = None, options: dict | None = None) -> tuple[int, dict]:
        super().reset(seed=seed, options=options)
        self._elapsed = 0
        return 0, {'reset': True}

    def step(self, action: int) -> Any:
        self._elapsed += 1
        truncated = self._elapsed == self._horizon
        return (
            self._elapsed,
            1.0,
            float(self._elapsed),
            False,
            truncated,
            {'elapsed': self._elapsed},
        )


class ModernApiTest(parameterized.TestCase):
    def _make_cost_vector(self, asynchronous: bool) -> SafetyAsyncVectorEnv | SafetySyncVectorEnv:
        factories = [partial(CostEnv, 1), partial(CostEnv, 2)]
        env = (
            SafetyAsyncVectorEnv(factories, context='spawn')
            if asynchronous
            else SafetySyncVectorEnv(factories)
        )
        self.addCleanup(env.close)
        env.reset(seed=17)
        return env

    @parameterized.named_parameters(('sync', False), ('async', True))
    def test_vector_same_step_preserves_terminal_cost(self, asynchronous: bool) -> None:
        env = self._make_cost_vector(asynchronous)
        actions = np.zeros(2, dtype=np.int64)
        _, _, costs, _, _, _ = cast('NativeStep', env.step(actions))
        np.testing.assert_array_equal(costs, [1.0, 1.0])

        _, _, costs, _, _, _ = cast('NativeStep', env.step(actions))
        np.testing.assert_array_equal(costs, [1.0, 2.0])

    @parameterized.named_parameters(('sync', False), ('async', True))
    def test_vector_same_step_retains_terminal_info(self, asynchronous: bool) -> None:
        env = self._make_cost_vector(asynchronous)
        obs, _, _, _, truncated, info = cast(
            'NativeStep',
            env.step(np.zeros(2, dtype=np.int64)),
        )
        np.testing.assert_array_equal(obs, [0, 1])
        np.testing.assert_array_equal(
            [truncated, info['_final_observation']],
            [[True, False], [True, False]],
        )
        self.assertEqual((info['final_observation'][0], info['final_info'][0]), (1, {'elapsed': 1}))

    @parameterized.product(use_gymnasium=[False, True], horizon=[2, -1])
    def test_episode_limit_override(self, use_gymnasium: bool, horizon: int) -> None:
        if use_gymnasium:
            env = gymnasium.make(
                'SafetyGymnasium2/SafetyPointGoal0Gymnasium-v0',
                max_episode_steps=horizon,
            )
            step_length = 5
        else:
            env = sg2.make(
                'SafetyPointGoal0-v0', config={'num_steps': 1}, max_episode_steps=horizon
            )
            step_length = 6
        self.addCleanup(env.close)

        obs, _ = env.reset(seed=8)
        repeated_obs, _ = env.reset(seed=8)
        np.testing.assert_array_equal(obs, repeated_obs)
        first_step = env.step([0.0, 0.0])
        self.assertEqual((len(first_step), bool(first_step[-2])), (step_length, False))
        self.assertEqual(bool(env.step([0.0, 0.0])[-2]), horizon == 2)

    def test_offscreen_viewer_reopens_after_reset_and_close(self) -> None:
        env = sg2.make('SafetyDoggoGoal0-v0', render_mode='rgb_array', width=72, height=48)
        self.addCleanup(env.close)
        for seed in range(2):
            env.reset(seed=seed)
            self.assertEqual(np.shape(env.render()), (48, 72, 3))
        env.close()
        env.reset(seed=0)
        self.assertEqual(np.shape(env.render()), (48, 72, 3))


if __name__ == '__main__':
    absltest.main()
