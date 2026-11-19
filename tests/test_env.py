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


class EnvironmentRenderTest(parameterized.TestCase):
    def _exercise_environment(self, env_id: str, render_mode: str) -> None:
        env = sg2.make(env_id, render_mode=render_mode)
        self.addCleanup(env.close)
        collect_frames = render_mode.endswith('_list')
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
                if not collect_frames:
                    env.render()
        if collect_frames:
            self.assertIsInstance(env.render(), list)

    @parameterized.product(
        agent_id=['Point', 'Car', 'Racecar', 'Ant', 'Doggo'],
        task=['Goal', 'Push', 'Button', 'Circle'],
        level=['0', '1', '2'],
        render_mode=['rgb_array', 'depth_array'],
    )
    def test_env_render(self, agent_id: str, task: str, level: str, render_mode: str) -> None:
        self._exercise_environment(f'Safety{agent_id}{task}{level}-v0', render_mode)

    @parameterized.product(
        agent_id=['Point', 'Car', 'Racecar', 'Ant', 'Doggo'],
        render_mode=['rgb_array', 'depth_array'],
    )
    def test_run_env_render(self, agent_id: str, render_mode: str) -> None:
        self._exercise_environment(f'Safety{agent_id}Run0-v0', render_mode)

    @parameterized.product(
        agent_id=['Humanoid', 'Ant', 'Hopper', 'HalfCheetah', 'Swimmer', 'Walker2d'],
        render_mode=['rgb_array', 'depth_array'],
        version=['v0', 'v1', 'v2'],
    )
    def test_velocity_env_render(self, agent_id: str, render_mode: str, version: str) -> None:
        self._exercise_environment(f'Safety{agent_id}Velocity-{version}', render_mode)

    @parameterized.product(render_mode=['rgb_array_list', 'depth_array_list'])
    def test_env_render_list(self, render_mode: str) -> None:
        self._exercise_environment('SafetyPointGoal0-v0', render_mode)

    @parameterized.product(
        render_mode=['rgb_array_list', 'depth_array_list'],
        version=['v0', 'v1', 'v2'],
    )
    def test_velocity_env_render_list(self, render_mode: str, version: str) -> None:
        self._exercise_environment(f'SafetyHumanoidVelocity-{version}', render_mode)


if __name__ == '__main__':
    absltest.main()
