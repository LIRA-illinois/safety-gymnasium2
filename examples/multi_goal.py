# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
# ==============================================================================
"""Examples for multi goal environments."""

import argparse

import safety_gymnasium2


def run_random(env_name: str) -> None:
    """Random run."""
    env = safety_gymnasium2.make(env_name, render_mode='human')
    observation_space = env.get_wrapper_attr('observation_space')
    action_space = env.get_wrapper_attr('action_space')
    obs, _ = env.reset()
    # Use below to specify seed.
    # obs, _ = env.reset(seed=0)
    terminated, truncated = {'agent_0': False}, {'agent_0': False}
    ep_ret, ep_cost = 0, 0
    while True:
        if terminated['agent_0'] or truncated['agent_0']:
            print(f'Episode Return: {ep_ret} \t Episode Cost: {ep_cost}')
            ep_ret, ep_cost = 0, 0
            obs, _ = env.reset()

        action_by_agent = {}
        for agent in env.get_wrapper_attr('agents'):
            assert observation_space(agent).contains(obs[agent])
            action_by_agent[agent] = action_space(agent).sample()
            assert action_space(agent).contains(action_by_agent[agent])

        obs, reward, cost, terminated, truncated, _ = env.step(action_by_agent)

        for agent in env.get_wrapper_attr('agents'):
            ep_ret += reward[agent]
            ep_cost += cost[agent]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', default='SafetyAntMultiGoal2-v0')
    args = parser.parse_args()
    run_random(args.env)
