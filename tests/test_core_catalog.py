# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

"""Registration and observation contracts for the core catalog."""

from __future__ import annotations

from itertools import product

import gymnasium as gym
import numpy as np
import safety_gymnasium2 as sg2
from absl.testing import absltest, parameterized
from safety_gymnasium2.utils.registration import safe_registry

_REMOVED_MARKERS = ('Building', 'FormulaOne', 'Race0', 'Race1', 'Race2', 'Vision')
_GYMNASIUM_NAMESPACE = 'SafetyGymnasium2/'
_NAVIGATION_TASKS = (
    'ButtonBase',
    'Button0',
    'Button1',
    'Button2',
    'CircleBase',
    'Circle0',
    'Circle1',
    'Circle2',
    'FadingEasy0',
    'FadingEasy1',
    'FadingEasy2',
    'FadingHard0',
    'FadingHard1',
    'FadingHard2',
    'GoalBase',
    'Goal0',
    'Goal1',
    'Goal2',
    'PushBase',
    'Push0',
    'Push1',
    'Push2',
    'RunBase',
    'Run0',
)


def _gymnasium_alias(env_id: str) -> str:
    name, version = env_id.rsplit('-', 1)
    return f'{_GYMNASIUM_NAMESPACE}{name}Gymnasium-{version}'


class CoreCatalogTest(parameterized.TestCase):
    def test_core_families_remain_registered(self) -> None:
        navigation = {
            f'Safety{robot}{task}-v0'
            for robot, task in product(
                ('Point', 'Car', 'Doggo', 'Racecar', 'Ant'), _NAVIGATION_TASKS
            )
        }
        navigation_debug = {
            f'Safety{robot}{task}Debug-v0'
            for robot, task in product(('Point', 'Car', 'Racecar'), _NAVIGATION_TASKS)
        }
        velocity = {
            f'Safety{robot}Velocity-v{version}'
            for robot, version in product(
                ('Ant', 'HalfCheetah', 'Hopper', 'Humanoid', 'Swimmer', 'Walker2d'), range(3)
            )
        }
        multi_goal = {
            f'Safety{robot}MultiGoal{level}-v0'
            for robot, level in product(('Point', 'Ant'), range(3))
        } | {f'SafetyPointMultiGoal{level}Debug-v0' for level in range(3)}
        single_agent_ids = navigation | navigation_debug | velocity
        self.assertSetEqual(set(safe_registry), single_agent_ids | multi_goal)
        self.assertSetEqual(
            {env_id for env_id in gym.registry if env_id.startswith(_GYMNASIUM_NAMESPACE)},
            {_gymnasium_alias(env_id) for env_id in single_agent_ids},
        )

    def test_removed_families_are_absent_from_both_registries(self) -> None:
        project_ids = set(safe_registry) | {
            env_id for env_id in gym.registry if env_id.startswith(_GYMNASIUM_NAMESPACE)
        }
        removed_ids = sorted(
            env_id for env_id in project_ids if any(marker in env_id for marker in _REMOVED_MARKERS)
        )
        self.assertEmpty(removed_ids)

    @parameterized.named_parameters(
        ('building_goal', 'SafetyPointBuildingGoal0-v0'),
        ('building_push', 'SafetyCarBuildingPush1-v0'),
        ('building_button', 'SafetyAntBuildingButton2-v0'),
        ('formula_one', 'SafetyRacecarFormulaOne0-v0'),
        ('race', 'SafetyRacecarRace0-v0'),
        ('vision', 'SafetyPointGoal0Vision-v0'),
        ('multi_goal_vision', 'SafetyAntMultiGoal0Vision-v0'),
    )
    def test_removed_ids_cannot_be_constructed(self, env_id: str) -> None:
        with self.assertRaises(gym.error.NameNotFound):
            sg2.make(env_id)
        with self.assertRaises(gym.error.NameNotFound):
            gym.make(_gymnasium_alias(env_id))

    @parameterized.named_parameters(
        ('rgb', 'rgb_array', (32, 48, 3)),
        ('depth', 'depth_array', (32, 48)),
    )
    def test_rendering_is_separate_from_vector_observations(
        self, render_mode: str, frame_shape: tuple[int, ...]
    ) -> None:
        env = sg2.make(
            'SafetyPointGoal0-v0',
            config={'observation_flatten': False},
            render_mode=render_mode,
            width=48,
            height=32,
        )
        self.addCleanup(env.close)
        observation, _ = env.reset(seed=17)
        self.assertTrue(env.observation_space.contains(observation))
        self.assertNotIn('vision', observation)
        self.assertEqual(np.shape(env.render()), frame_shape)


if __name__ == '__main__':
    absltest.main()
