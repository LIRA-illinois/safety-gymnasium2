# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from functools import partial

import gymnasium
import numpy as np
import pytest

import safety_gymnasium2
from safety_gymnasium2.vector import SafetyAsyncVectorEnv, SafetySyncVectorEnv


class CostEnv(gymnasium.Env):
    """Small deterministic environment with observable terminal costs."""

    observation_space = gymnasium.spaces.Discrete(5)
    action_space = gymnasium.spaces.Discrete(2)

    def __init__(self, horizon):
        self.horizon = horizon
        self.elapsed = 0

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.elapsed = 0
        return 0, {'reset': True}

    def step(self, action):
        self.elapsed += 1
        truncated = self.elapsed == self.horizon
        return self.elapsed, 1.0, float(self.elapsed), False, truncated, {'elapsed': self.elapsed}


@pytest.fixture(params=[SafetySyncVectorEnv, SafetyAsyncVectorEnv])
def cost_vector(request):
    env = request.param([partial(CostEnv, 1), partial(CostEnv, 2)])
    try:
        env.reset(seed=17)
        yield env
    finally:
        env.close()


def test_vector_same_step_preserves_terminal_cost(cost_vector):
    actions = np.zeros(2, dtype=np.int64)
    _, _, costs, _, _, _ = cost_vector.step(actions)
    np.testing.assert_array_equal(costs, [1.0, 1.0])

    _, _, costs, _, _, _ = cost_vector.step(actions)
    np.testing.assert_array_equal(costs, [1.0, 2.0])


def test_vector_same_step_retains_terminal_info(cost_vector):
    obs, _, _, _, truncated, info = cost_vector.step(np.zeros(2, dtype=np.int64))
    np.testing.assert_array_equal(obs, [0, 1])
    np.testing.assert_array_equal(
        [truncated, info['_final_observation']],
        [[True, False], [True, False]],
    )
    assert (info['final_observation'][0], info['final_info'][0]) == (1, {'elapsed': 1})


@pytest.mark.parametrize(
    ('factory', 'env_id', 'step_length'),
    [
        (safety_gymnasium2.make, 'SafetyPointGoal0-v0', 6),
        (gymnasium.make, 'SafetyGymnasium2/SafetyPointGoal0Gymnasium-v0', 5),
    ],
)
@pytest.mark.parametrize(('horizon', 'second_step_truncated'), [(2, True), (-1, False)])
def test_episode_limit_override(factory, env_id, step_length, horizon, second_step_truncated):
    env = factory(env_id, config={'num_steps': 1}, max_episode_steps=horizon)
    try:
        obs, _ = env.reset(seed=8)
        repeated_obs, _ = env.reset(seed=8)
        np.testing.assert_array_equal(obs, repeated_obs)
        first_step = env.step([0.0, 0.0])
        assert (len(first_step), bool(first_step[-2])) == (step_length, False)
        assert bool(env.step([0.0, 0.0])[-2]) == second_step_truncated
    finally:
        env.close()


def test_offscreen_viewer_reopens_after_reset_and_close():
    env = safety_gymnasium2.make('SafetyDoggoGoal0-v0', render_mode='rgb_array', width=72, height=48)
    try:
        for seed in range(2):
            env.reset(seed=seed)
            assert env.render().shape == (48, 72, 3)
        env.close()
        env.reset(seed=0)
        assert env.render().shape == (48, 72, 3)
    finally:
        env.close()
