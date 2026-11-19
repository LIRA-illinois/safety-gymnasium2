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
from typing import cast

import safety_gymnasium2 as sg2
from absl.testing import absltest, parameterized
from safety_gymnasium2.utils._types import NativeStep


class VisionEnvironmentTest(parameterized.TestCase):
    def _exercise_environment(self, env_id: str) -> None:
        env = sg2.make(env_id)
        self.addCleanup(env.close)
        for _ in range(2):
            observation, _ = env.reset()
            for _ in range(2):
                self.assertTrue(env.observation_space.contains(observation))
                action = env.action_space.sample()
                self.assertTrue(env.action_space.contains(action))
                observation, reward, cost, _, _, _ = cast(
                    'NativeStep',
                    env.step(action),
                )
                self.assertIsInstance(reward, Real)
                self.assertIsInstance(cost, Real)

    @parameterized.product(
        agent_id=['Point', 'Car', 'Racecar', 'Ant'],
        task=[
            'Goal',
            'Push',
            'Button',
            'Race',
            'FadingEasy',
            'FadingHard',
            'BuildingGoal',
            'BuildingPush',
            'BuildingButton',
            'FormulaOne',
        ],
        level=['0', '1', '2'],
    )
    def test_vision_env(self, agent_id: str, task: str, level: str) -> None:
        self._exercise_environment(f'Safety{agent_id}{task}{level}Vision-v0')

    @parameterized.product(agent_id=['Point', 'Car', 'Racecar', 'Ant'])
    def test_run_vision_env(self, agent_id: str) -> None:
        self._exercise_environment(f'Safety{agent_id}Run0Vision-v0')


if __name__ == '__main__':
    absltest.main()
