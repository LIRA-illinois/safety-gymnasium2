# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
# ==============================================================================
"""Multiprocessing vectorization of native safety environments."""

from __future__ import annotations

from collections.abc import Callable, Sequence

from gymnasium import Env, Space
from gymnasium.vector import AsyncVectorEnv, AutoresetMode

from safety_gymnasium2.vector._compatibility import (
    SafetyVectorRender,
    restore_costs,
    wrap_factories,
)


class SafetyAsyncVectorEnv(SafetyVectorRender, AsyncVectorEnv):
    """Run native safety environments in parallel with same-step autoreset."""

    def __init__(
        self,
        env_fns: Sequence[Callable[[], Env]],
        observation_space: Space | None = None,
        action_space: Space | None = None,
        shared_memory: bool = True,
        copy: bool = True,
        context: str | None = None,
        daemon: bool = True,
        worker: Callable[..., None] | None = None,
    ) -> None:
        """Create workers that use Gymnasium's public vectorization API."""
        super().__init__(
            wrap_factories(env_fns, observation_space, action_space),
            shared_memory=shared_memory,
            copy=copy,
            context=context,
            daemon=daemon,
            worker=worker,
            autoreset_mode=AutoresetMode.SAME_STEP,
        )

    def step_wait(self, timeout: float | None = None):
        """Read all worker transitions and return their native safety costs."""
        return restore_costs(super().step_wait(timeout))
