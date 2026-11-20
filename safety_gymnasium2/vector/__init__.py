# Modified for Safety Gymnasium 2.
# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
# ==============================================================================
"""The vectorized Safety-Gymnasium wrapper."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from functools import partial
from typing import Any, cast

import gymnasium
from gymnasium.envs.registration import EnvSpec
from gymnasium.vector import VectorEnv

from safety_gymnasium2.utils.registration import make as safety_make
from safety_gymnasium2.utils.registration import spec
from safety_gymnasium2.vector.async_vector_env import SafetyAsyncVectorEnv
from safety_gymnasium2.vector.sync_vector_env import SafetySyncVectorEnv

__all__ = ['SafetyAsyncVectorEnv', 'SafetySyncVectorEnv', 'VectorEnv', 'make']
_EnvWrapper = Callable[[gymnasium.Env], gymnasium.Env]


def _make_vector_member(
    env_spec: EnvSpec,
    wrappers: Iterable[_EnvWrapper],
    disable_env_checker: bool | None,
    options_by_name: Mapping[str, Any],
) -> gymnasium.Env:
    env = safety_make(
        env_spec,
        autoreset=False,
        disable_env_checker=disable_env_checker,
        **options_by_name,
    )
    for wrapper in wrappers:
        env = wrapper(env)
    return env


def make(
    env_id: str,
    num_envs: int = 1,
    asynchronous: bool = True,
    wrappers: _EnvWrapper | Iterable[_EnvWrapper] | None = None,
    disable_env_checker: bool | None = None,
    *,
    multiprocessing_context: str | None = None,
    **kwargs: Any,
) -> VectorEnv:
    """Create a vectorized environment from multiple copies of an environment, from its id.

    Example::

        >>> import safety_gymnasium2
        >>> env = safety_gymnasium2.vector.make('SafetyPointGoal1-v0', num_envs=3)
        >>> env.observation_space
        Box(-inf, inf, (3, 60), float64)
        >>> env.action_space
        Box(-1.0, 1.0, (3, 2), float64)

    Args:
        env_id: The environment id. This must be a valid ID from the registry.
        num_envs: Number of copies of the environment.
        asynchronous: If `True`, wraps the environments in an :class:`AsyncVectorEnv`
        (which uses `multiprocessing`_ to run the environments in parallel). If ``False``,
        wraps the environments in a :class:`SyncVectorEnv`.
        wrappers: If not ``None``, then apply the wrappers to each internal environment during creation.
        disable_env_checker: If to run the env checker for the first environment only.
        None will default to the environment spec `disable_env_checker` parameter
        (that is by default False), otherwise will run according to this argument (True=not run, False=run)
        multiprocessing_context: Start method for asynchronous workers, such as ``spawn``.
            When omitted, multiprocessing uses the platform default.
        **kwargs: Keyword arguments passed to ``safety_gymnasium2.make``.
    """

    if num_envs <= 0:
        raise ValueError('num_envs must be positive.')
    if kwargs.pop('autoreset', False):
        raise ValueError('Vector environments already reset automatically on the terminal step.')
    if multiprocessing_context is not None and not asynchronous:
        raise ValueError('multiprocessing_context requires asynchronous vectorization.')

    per_environment_wrappers = (
        (cast('_EnvWrapper', wrappers),) if callable(wrappers) else tuple(wrappers or ())
    )

    # Spawned workers do not inherit programmatically registered environment specs.
    env_spec = spec(env_id)
    env_fns = [
        partial(
            _make_vector_member,
            env_spec,
            per_environment_wrappers,
            disable_env_checker if index == 0 else True,
            kwargs,
        )
        for index in range(num_envs)
    ]
    if asynchronous:
        return SafetyAsyncVectorEnv(env_fns, context=multiprocessing_context)
    return SafetySyncVectorEnv(env_fns)
