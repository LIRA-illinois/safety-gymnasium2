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
"""Wrappers for converting between Safety-Gymnasium and Gymnasium environments."""


from typing import TYPE_CHECKING, cast

import gymnasium
from gymnasium import logger
from gymnasium.core import ActType

if TYPE_CHECKING:
    from safety_gymnasium2.utils._types import NativeStep


class SafetyGymnasium2Gymnasium(gymnasium.Wrapper):
    """A class that converts a Safety-Gymnasium environment to a Gymnasium environment."""

    def step(self, action: ActType):
        obs, reward, cost, terminated, truncated, info = cast('NativeStep', self.env.step(action))
        if 'cost' in info:
            logger.warn(
                'The info dict already contains a cost. '
                'Overwriting it may cause unexpected behavior.',
            )
        return obs, reward, terminated, truncated, {**info, 'cost': cost}


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


class _RegisteredGymnasiumAlias(SafetyGymnasium2Gymnasium):
    """The conversion is part of the registered environment itself."""

    @property
    def spec(self):
        """Return the specification installed by Gymnasium on the base environment."""
        return self.unwrapped.spec


def make_gymnasium_environment(env_id, **kwargs):
    """Instantiate a five-value alias and leave time limits to Gymnasium."""
    from safety_gymnasium2.utils.registration import _create_environment, spec

    env, render_wrapper = _create_environment(spec(env_id), kwargs)
    if render_wrapper is not None:
        env = render_wrapper(env)
    return _RegisteredGymnasiumAlias(env)
