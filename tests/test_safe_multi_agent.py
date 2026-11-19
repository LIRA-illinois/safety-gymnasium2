# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from __future__ import annotations

from typing import cast

import safety_gymnasium2 as sg2
from absl.testing import absltest, parameterized
from safety_gymnasium2.utils._types import NativeStep


class MultiAgentTest(parameterized.TestCase):
    @parameterized.named_parameters(
        ('ant_2x4', 'Ant', '2x4'),
        ('ant_4x2', 'Ant', '4x2'),
        ('half_cheetah_6x1', 'HalfCheetah', '6x1'),
        ('half_cheetah_2x3', 'HalfCheetah', '2x3'),
        ('hopper', 'Hopper', '3x1'),
        ('humanoid', 'Humanoid', '9|8'),
        ('swimmer', 'Swimmer', '2x1'),
        ('walker', 'Walker2d', '2x3'),
    )
    def test_safe_ma(self, scenario: str, agent_conf: str) -> None:
        env = sg2.make_ma(scenario, agent_conf)
        self.addCleanup(env.close)
        for _ in range(2):
            obs, _ = env.reset()
            for _ in range(2):
                self.assertTrue(
                    all(env.observation_space(agent).contains(obs[agent]) for agent in env.agents)
                )
                actions_by_agent = {agent: env.action_space(agent).sample() for agent in env.agents}
                self.assertTrue(
                    all(
                        env.action_space(agent).contains(actions_by_agent[agent])
                        for agent in env.agents
                    ),
                )
                obs, _, _, _, _, _ = env.step(actions_by_agent)

    @parameterized.product(
        agent_id=['Point', 'Ant'],
        level=['0', '1', '2'],
        render_mode=['rgb_array', 'depth_array'],
    )
    def test_multi_goal(self, agent_id: str, level: str, render_mode: str) -> None:
        env = sg2.make(f'Safety{agent_id}MultiGoal{level}-v0', render_mode=render_mode)
        self.addCleanup(env.close)
        action_space = env.get_wrapper_attr('action_space')
        observation_space = env.get_wrapper_attr('observation_space')
        for _ in range(2):
            obs, _ = env.reset()
            for _ in range(2):
                agents = env.get_wrapper_attr('agents')
                self.assertTrue(
                    all(observation_space(agent).contains(obs[agent]) for agent in agents)
                )
                actions_by_agent = {agent: action_space(agent).sample() for agent in agents}
                self.assertTrue(
                    all(action_space(agent).contains(actions_by_agent[agent]) for agent in agents)
                )
                obs, reward_by_agent, cost_by_agent, _, _, _ = cast(
                    'NativeStep',
                    env.step(actions_by_agent),
                )
                stepped_agents = set(env.get_wrapper_attr('agents'))
                self.assertEmpty(stepped_agents - (reward_by_agent.keys() & cost_by_agent.keys()))
                env.render()


if __name__ == '__main__':
    absltest.main()
