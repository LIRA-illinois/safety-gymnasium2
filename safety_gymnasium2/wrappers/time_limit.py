# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
# ==============================================================================
"""Wrapper for limiting the time steps of an environment."""

from typing import TYPE_CHECKING, cast

from gymnasium.error import ResetNeeded
from gymnasium.wrappers import TimeLimit

if TYPE_CHECKING:
    from safety_gymnasium2.utils._types import NativeStep


class SafeTimeLimit(TimeLimit):
    """Truncate a safety episode at its configured horizon."""

    def step(self, action):
        """Step the environment and mark truncation once the horizon is reached."""
        if self._elapsed_steps is None:
            raise ResetNeeded('Call reset before stepping a time-limited environment.')
        result = cast('NativeStep', self.env.step(action))
        observation, reward, cost, terminated, truncated, info = result
        self._elapsed_steps += 1

        if self._elapsed_steps >= self._max_episode_steps:
            truncated = dict.fromkeys(truncated, True) if isinstance(truncated, dict) else True

        return observation, reward, cost, terminated, truncated, info
