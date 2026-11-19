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
"""Serial vectorization of native safety environments."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from gymnasium import Env, Space, error
from gymnasium.vector import AutoresetMode, SyncVectorEnv

from safety_gymnasium2.vector._compatibility import SafetyVectorRender, restore_costs, wrap_factories


class SafetySyncVectorEnv(SafetyVectorRender, SyncVectorEnv):
    """Run native safety environments serially with same-step autoreset."""

    def __init__(
        self,
        env_fns: Iterable[Callable[[], Env]],
        observation_space: Space | None = None,
        action_space: Space | None = None,
        copy: bool = True,
    ) -> None:
        """Create environments and batch their spaces and transitions."""
        super().__init__(
            wrap_factories(env_fns, observation_space, action_space),
            copy=copy,
            autoreset_mode=AutoresetMode.SAME_STEP,
        )
        self._pending_actions: Any = None

    def step(self, actions):
        """Step all environments while preserving their native safety costs."""
        return restore_costs(super().step(actions))

    def step_async(self, actions: Any) -> None:
        """Stage actions for a subsequent step_wait call."""
        self._pending_actions = actions

    def step_wait(self):
        """Step all environments with the staged actions."""
        if self._pending_actions is None:
            raise error.NoAsyncCallError('Call step_async before step_wait.', 'step')
        actions, self._pending_actions = self._pending_actions, None
        return self.step(actions)
