# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
# ==============================================================================
"""Test copy of environments."""

from copy import deepcopy

import numpy as np

import helpers
import safety_gymnasium2 as sg2


def _assert_equal_step(actual, expected):
    observation, *outcomes = actual
    expected_observation, *expected_outcomes = expected
    np.testing.assert_array_equal(observation, expected_observation)
    assert outcomes == expected_outcomes


@helpers.parametrize(
    agent_id=['Point'],
    env_id=['Goal'],
    level=['0'],
)
def test_equal_outcomes_branch(agent_id, env_id, level):
    """Test copyable env."""
    env_name = 'SafetyGymnasium2/Safety' + agent_id + env_id + level + 'Gymnasium' + '-v0'
    env1 = sg2.gymnasium_make(env_name)
    env1.reset(seed=29)
    env1.action_space.seed(29)

    env2 = deepcopy(env1)
    move = env1.action_space.sample()
    expected = env1.step(move)
    _assert_equal_step(env2.step(move), expected)

    env3 = deepcopy(env1)
    env4 = deepcopy(env2)
    move = env1.action_space.sample()
    expected = env1.step(move)
    for env in (env2, env3, env4):
        _assert_equal_step(env.step(move), expected)


@helpers.parametrize(
    agent_id=['Point', 'Car', 'Doggo'],
    env_id=['Goal'],
    level=['0', '2'],
)
def test_equal_outcomes_long(agent_id, env_id, level):
    """Test SafetyGymnasium2Gymnasium env."""
    env_name = 'SafetyGymnasium2/Safety' + agent_id + env_id + level + 'Gymnasium' + '-v0'
    env1 = sg2.gymnasium_make(env_name)
    env1.reset(seed=29)
    env1.action_space.seed(29)

    for _ in range(16):
        env1.step(env1.action_space.sample())

    env2 = deepcopy(env1)
    for _ in range(32):
        move = env1.action_space.sample()
        expected = env1.step(move)
        _assert_equal_step(env2.step(move), expected)
