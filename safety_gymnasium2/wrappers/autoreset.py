# Modified for Safety Gymnasium 2.
# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
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
"""Automatically reset a safety environment on the terminal step."""

from typing import TYPE_CHECKING, cast

from gymnasium import Env, Wrapper
from gymnasium.utils import RecordConstructorArgs

if TYPE_CHECKING:
    from safety_gymnasium2.utils._types import NativeStep


class SafeAutoResetWrapper(Wrapper, RecordConstructorArgs):
    """Return the reset observation while preserving the terminal transition."""

    def __init__(self, env: Env) -> None:
        """Wrap an environment and keep its same-step autoreset behavior."""
        RecordConstructorArgs.__init__(self)
        Wrapper.__init__(self, env)

    def step(self, action):
        """Step the environment and reset it when the episode ends."""
        obs, reward, cost, terminated, truncated, info = cast('NativeStep', self.env.step(action))
        if isinstance(terminated, dict):
            done = all(terminated[agent] or truncated[agent] for agent in terminated)
        else:
            done = terminated or truncated
        if done:
            new_obs, new_info = self.env.reset()
            if 'final_observation' in new_info or 'final_info' in new_info:
                raise ValueError('Reset info must not use final_observation or final_info.')
            new_info = {**new_info, 'final_observation': obs, 'final_info': info}
            info = new_info
            obs = new_obs
        return obs, reward, cost, terminated, truncated, info
