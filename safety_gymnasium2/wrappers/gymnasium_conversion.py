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
"""Wrappers for converting between Safety-Gymnasium and Gymnasium environments."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, SupportsFloat, cast

import gymnasium
from gymnasium import logger
from gymnasium.core import ActType

if TYPE_CHECKING:
    from safety_gymnasium2.utils._types import NativeStep


def _gymnasium_step(
    transition: NativeStep,
) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
    obs, reward, cost, terminated, truncated, info = transition
    if 'cost' in info:
        logger.warn(
            'The info dict already contains a cost. Overwriting it may cause unexpected behavior.',
        )
    return obs, reward, terminated, truncated, {**info, 'cost': cost}


class SafetyGymnasium2Gymnasium(gymnasium.Wrapper):
    """A class that converts a Safety-Gymnasium environment to a Gymnasium environment."""

    def step(self, action: ActType):
        return _gymnasium_step(cast('NativeStep', self.env.step(action)))


class Gymnasium2SafetyGymnasium(gymnasium.Wrapper):
    """A class that converts a Gymnasium environment to a Safety-Gymnasium environment."""

    def step(self, action: ActType):
        obs, reward, terminated, truncated, info = super().step(action)
        try:
            cost = info['cost']
        except KeyError as ex:
            raise ValueError(
                'The info dict does not contain a cost which is required by Safety-Gymnasium.',
            ) from ex
        return obs, reward, cost, terminated, truncated, info


class _RegisteredGymnasiumAlias(gymnasium.Env):
    """A registered Gymnasium environment backed by a native safety environment.

    Attributes:
        native_env: The safety environment that supplies six-value transitions.
    """

    def __init__(self, native_env: gymnasium.Env) -> None:
        self.native_env = native_env
        self.action_space = native_env.action_space
        self.observation_space = native_env.observation_space
        self.metadata = native_env.metadata.copy()
        self.render_mode = native_env.render_mode

    def reset(
        self,
        *,
        seed: int | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> tuple[Any, dict[str, Any]]:
        """Reset the alias and its native environment with the supplied seed."""
        super().reset(seed=seed)
        native_options = None if options is None else dict(options)
        return self.native_env.reset(seed=seed, options=native_options)

    def step(self, action: Any) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        """Return a Gymnasium transition with the native safety cost in info."""
        return _gymnasium_step(cast('NativeStep', self.native_env.step(action)))

    def render(self) -> Any:
        """Render through the native environment."""
        return self.native_env.render()

    def close(self) -> None:
        """Close the native environment."""
        self.native_env.close()


def make_gymnasium_environment(env_id: str, **kwargs: Any) -> gymnasium.Env:
    """Instantiate a five-value alias and leave time limits to Gymnasium."""
    from safety_gymnasium2.utils.registration import _create_environment, spec

    config = kwargs.get('config')
    if isinstance(config, Mapping) and 'num_steps' in config:
        raise ValueError('Gymnasium aliases use max_episode_steps instead of config["num_steps"].')
    env, render_wrapper = _create_environment(spec(env_id), kwargs)
    if render_wrapper is not None:
        env = render_wrapper(env)
    return _RegisteredGymnasiumAlias(env)
