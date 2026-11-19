# Copyright 2022-2024 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

import numpy as np
import safety_gymnasium2 as sg2
from absl.testing import absltest, parameterized
from safety_gymnasium2.tasks.safe_navigation.button.button_configs import button_level0
from safety_gymnasium2.tasks.safe_navigation.circle.circle_configs import circle_level0
from safety_gymnasium2.tasks.safe_navigation.goal.goal_configs import goal_level0
from safety_gymnasium2.tasks.safe_navigation.push.push_configs import push_level0
from safety_gymnasium2.tasks.safe_navigation.run.run_configs import run_level0
from safety_gymnasium2.utils._types import NativeStep


class ConfigEnvironmentTest(parameterized.TestCase):
    @parameterized.named_parameters(
        ('goal', 'SafetyPointGoal0-v0', 'SafetyPointGoalBase-v0', goal_level0),
        ('push', 'SafetyPointPush0-v0', 'SafetyPointPushBase-v0', push_level0),
        ('button', 'SafetyPointButton0-v0', 'SafetyPointButtonBase-v0', button_level0),
        ('run', 'SafetyPointRun0-v0', 'SafetyPointRunBase-v0', run_level0),
        ('circle', 'SafetyPointCircle0-v0', 'SafetyPointCircleBase-v0', circle_level0),
    )
    def test_config(
        self,
        env_id: str,
        base_env_id: str,
        config: Mapping[str, Any],
    ) -> None:
        env = sg2.make(base_env_id, config=config)
        self.addCleanup(env.close)
        registered = sg2.make(env_id)
        self.addCleanup(registered.close)

        env.reset(seed=42)
        registered.reset(seed=42)
        registered.action_space.seed(42)
        for _ in range(4):
            action = registered.action_space.sample()
            obs, reward, cost, terminated, truncated, _ = cast('NativeStep', env.step(action))
            expected, expected_reward, expected_cost, expected_term, expected_trunc, _ = cast(
                'NativeStep',
                registered.step(action),
            )
            np.testing.assert_allclose(obs, expected, rtol=1e-5, atol=1e-8)
            np.testing.assert_allclose(
                (reward, cost),
                (expected_reward, expected_cost),
                rtol=1e-5,
                atol=1e-8,
            )
            self.assertEqual((terminated, truncated), (expected_term, expected_trunc))
            if terminated or truncated:
                break


if __name__ == '__main__':
    absltest.main()
