# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
# ==============================================================================
"""Test multi-agent environments."""

import pytest

import helpers
import safety_gymnasium2


@pytest.mark.parametrize(
    ('scenario', 'agent_conf'),
    [
        ('Ant', '2x4'),
        ('Ant', '4x2'),
        ('HalfCheetah', '6x1'),
        ('HalfCheetah', '2x3'),
        ('Hopper', '3x1'),
        ('Humanoid', '9|8'),
        ('Swimmer', '2x1'),
        ('Walker2d', '2x3'),
    ],
)
def test_safe_ma(scenario, agent_conf):
    """Check reset and step for each Robotics agent configuration."""
    env = safety_gymnasium2.make_ma(scenario, agent_conf)
    try:
        obs, _ = env.reset()
        for step in range(4):
            if step == 2:
                obs, _ = env.reset()

            action_by_agent = {}
            for agent in env.agents:
                assert env.observation_space(agent).contains(obs[agent])
                action_by_agent[agent] = env.action_space(agent).sample()
                assert env.action_space(agent).contains(action_by_agent[agent])

            obs, _, _, _, _, _ = env.step(action_by_agent)
    finally:
        env.close()


@helpers.parametrize(
    agent_id=['Point', 'Ant'],
    env_id=['MultiGoal'],
    level=['0', '1', '2'],
    render_mode=['rgb_array', 'depth_array'],
)
def test_multi_goal(agent_id, env_id, level, render_mode):
    """Random run."""
    env_name = 'Safety' + agent_id + env_id + level + '-v0'
    env = safety_gymnasium2.make(env_name, render_mode=render_mode)
    obs, _ = env.reset()
    # Use below to specify seed.
    # obs, _ = env.reset(seed=0)
    _, _ = {'agent_0': False}, {'agent_0': False}
    ep_ret, ep_cost = 0, 0
    for step in range(4):
        if step == 2:
            print(f'Episode Return: {ep_ret} \t Episode Cost: {ep_cost}')
            ep_ret, ep_cost = 0, 0
            obs, _ = env.reset()

        action_by_agent = {}
        for agent in env.agents:
            assert env.observation_space(agent).contains(obs[agent])
            action_by_agent[agent] = env.action_space(agent).sample()
            assert env.action_space(agent).contains(action_by_agent[agent])

        obs, reward, cost, _, _, _ = env.step(action_by_agent)

        for agent in env.agents:
            ep_ret += reward[agent]
            ep_cost += cost[agent]

        env.render()
