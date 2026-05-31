# Copyright 2022-2023 LIRA. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Test custom task dynamic loading."""

import gymnasium
import pytest

import safety_gymnasium
from safety_gymnasium.tasks.safe_navigation.goal.goal_level0 import GoalLevel0


class DummyCustomTask(GoalLevel0):
    """A dummy custom task subclassing GoalLevel0 to verify loading."""

    def __init__(self, config) -> None:
        super().__init__(config=config)
        self.custom_marker = "verified"


def test_custom_task_class_object():
    """Test loading a custom task passed directly as a class object."""
    # We can use an existing environment config but inject task_class
    env_id = 'SafetyPointGoal0-v0'
    env = safety_gymnasium.make(env_id, config={'task_class': DummyCustomTask})
    
    # Verify the task instance is of DummyCustomTask
    # Unwrap TimeLimit/OrderEnforcing if present
    unwrapped = env.unwrapped
    assert type(unwrapped.task).__name__ == "DummyCustomTask"
    assert unwrapped.task.custom_marker == "verified"
    
    obs, _ = env.reset()
    assert env.observation_space.contains(obs)
    env.close()


def test_custom_task_class_string_path_colon():
    """Test loading a custom task passed as a module path string with colon."""
    env_id = 'SafetyPointGoal0-v0'
    env = safety_gymnasium.make(
        env_id, 
        config={'task_class': 'tests.test_custom_task:DummyCustomTask'}
    )
    
    unwrapped = env.unwrapped
    assert type(unwrapped.task).__name__ == "DummyCustomTask"
    assert unwrapped.task.custom_marker == "verified"
    
    obs, _ = env.reset()
    assert env.observation_space.contains(obs)
    env.close()


def test_custom_task_name_string_path_dot():
    """Test loading a custom task passed as a module path string with dot in task_name."""
    env_id = 'SafetyPointGoal0-v0'
    env = safety_gymnasium.make(
        env_id, 
        config={'task_name': 'tests.test_custom_task.DummyCustomTask'}
    )
    
    unwrapped = env.unwrapped
    assert type(unwrapped.task).__name__ == "DummyCustomTask"
    assert unwrapped.task.custom_marker == "verified"
    
    obs, _ = env.reset()
    assert env.observation_space.contains(obs)
    env.close()
