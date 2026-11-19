# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from __future__ import annotations

from copy import deepcopy
from typing import Any

import gymnasium
import numpy as np
import safety_gymnasium2 as sg2
from absl.testing import absltest, parameterized


class DeepCopyTest(parameterized.TestCase):
    def _make_env(self, agent_id: str, level: str) -> gymnasium.Env:
        env = sg2.gymnasium_make(f'SafetyGymnasium2/Safety{agent_id}Goal{level}Gymnasium-v0')
        self.addCleanup(env.close)
        env.reset(seed=29)
        env.action_space.seed(29)
        return env

    def _copy_env(self, env: gymnasium.Env) -> gymnasium.Env:
        copied = deepcopy(env)
        self.addCleanup(copied.close)
        return copied

    def _assert_equal_step(self, actual: tuple[Any, ...], expected: tuple[Any, ...]) -> None:
        observation, *outcomes = actual
        expected_observation, *expected_outcomes = expected
        np.testing.assert_array_equal(observation, expected_observation)
        self.assertEqual(outcomes, expected_outcomes)

    def test_equal_outcomes_branch(self) -> None:
        env = self._make_env('Point', '0')
        branch = self._copy_env(env)
        action = env.action_space.sample()
        expected = env.step(action)
        self._assert_equal_step(branch.step(action), expected)

        branches = branch, self._copy_env(env), self._copy_env(branch)
        action = env.action_space.sample()
        expected = env.step(action)
        for copy in branches:
            self._assert_equal_step(copy.step(action), expected)

    @parameterized.product(agent_id=['Point', 'Car', 'Doggo'], level=['0', '2'])
    def test_equal_outcomes_long(self, agent_id: str, level: str) -> None:
        env = self._make_env(agent_id, level)
        for _ in range(16):
            env.step(env.action_space.sample())

        copied = self._copy_env(env)
        for _ in range(32):
            action = env.action_space.sample()
            expected = env.step(action)
            self._assert_equal_step(copied.step(action), expected)


if __name__ == '__main__':
    absltest.main()
