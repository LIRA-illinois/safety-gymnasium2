# Modified for Safety Gymnasium 2.
# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from __future__ import annotations

from numbers import Real

import gymnasium
import safety_gymnasium2 as sg2
from absl.testing import absltest


class GymnasiumConversionTest(absltest.TestCase):
    def _check_rollout(self, env: gymnasium.Env, step_length: int) -> None:
        self.addCleanup(env.close)
        for _ in range(2):
            observation, _ = env.reset()
            for _ in range(2):
                self.assertTrue(env.observation_space.contains(observation))
                action = env.action_space.sample()
                self.assertTrue(env.action_space.contains(action))
                transition = env.step(action)
                self.assertLen(transition, step_length)
                observation = transition[0]
                cost = transition[-1]['cost'] if step_length == 5 else transition[2]
                self.assertIsInstance(transition[1], Real)
                self.assertIsInstance(cost, Real)

    def test_navigation_env(self) -> None:
        env = gymnasium.make('SafetyGymnasium2/SafetyPointGoal0Gymnasium-v0')
        self._check_rollout(env, step_length=5)

    def test_convert_api(self) -> None:
        env = gymnasium.make('SafetyGymnasium2/SafetyPointGoal0Gymnasium-v0')
        clipped = gymnasium.wrappers.ClipAction(env)
        native = sg2.wrappers.Gymnasium2SafetyGymnasium(clipped)
        self._check_rollout(native, step_length=6)

    def test_with_wrappers(self) -> None:
        env = sg2.wrappers.with_gymnasium_wrappers(
            sg2.make('SafetyPointGoal0-v0'),
            gymnasium.wrappers.ClipAction,
        )
        self._check_rollout(env, step_length=6)


if __name__ == '__main__':
    absltest.main()
