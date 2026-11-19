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
"""Adapt native safety transitions for Gymnasium vectorization."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from functools import partial
from typing import TYPE_CHECKING, Any, cast

import gymnasium
import numpy as np

from safety_gymnasium2.vector.utils.tile_images import tile_images

if TYPE_CHECKING:
    from safety_gymnasium2.utils._types import NativeStep


_COST_KEY = 'safety_gymnasium2_cost'
_COST_MASK = f'_{_COST_KEY}'


class _VectorMember(gymnasium.Wrapper):
    """Put the cost in a private info field for the upstream vector step."""

    def __init__(
        self,
        env: gymnasium.Env,
        observation_space: gymnasium.Space | None,
        action_space: gymnasium.Space | None,
    ) -> None:
        super().__init__(env)
        self.metadata = env.metadata.copy()
        if observation_space is not None and env.observation_space != observation_space:
            env.close()
            raise ValueError('Vector member observation space does not match the requested space.')
        if action_space is not None and env.action_space != action_space:
            env.close()
            raise ValueError('Vector member action space does not match the requested space.')

    def step(self, action):
        """Return a standard Gymnasium transition with an internal cost field."""
        obs, reward, cost, terminated, truncated, info = cast('NativeStep', self.env.step(action))
        if _COST_KEY in info or _COST_MASK in info:
            raise ValueError(f'{_COST_KEY!r} is reserved in vector environment info.')
        return obs, reward, terminated, truncated, {**info, _COST_KEY: float(cost)}


def _make_member(
    env_fn: Callable[[], gymnasium.Env],
    observation_space: gymnasium.Space | None,
    action_space: gymnasium.Space | None,
) -> gymnasium.Env:
    return _VectorMember(env_fn(), observation_space, action_space)


def wrap_factories(
    env_fns: Iterable[Callable[[], gymnasium.Env]],
    observation_space: gymnasium.Space | None,
    action_space: gymnasium.Space | None,
) -> Sequence[Callable[[], gymnasium.Env]]:
    """Adapt each native environment factory for a Gymnasium vectorizer."""
    factories = [
        partial(_make_member, factory, observation_space, action_space) for factory in env_fns
    ]
    if not factories:
        raise ValueError('At least one environment is required for vectorization.')
    return factories


def _info_at(infos: Mapping[str, Any], index: int) -> dict[str, Any]:
    """Unbatch an individual lane's info using the Gymnasium presence masks."""
    result = {}
    for key, values in infos.items():
        mask = infos.get(f'_{key}')
        if mask is not None and mask[index]:
            result[key] = _info_at(values, index) if isinstance(values, dict) else values[index]
    return result


def restore_costs(result):
    """Restore native costs and terminal info after an upstream vector step."""
    observations, rewards, terminated, truncated, infos = result
    costs = np.zeros(rewards.shape, dtype=np.float64)
    if _COST_KEY in infos:
        active = infos.pop(_COST_MASK)
        costs[active] = infos.pop(_COST_KEY)[active]

    if 'final_info' in infos:
        final_info = infos['final_info']
        done = infos['_final_info']
        costs[done] = final_info.pop(_COST_KEY)[done]
        final_info.pop(_COST_MASK)
        terminal_infos = np.full(rewards.shape, None, dtype=object)
        for index in np.flatnonzero(done):
            terminal_infos[index] = _info_at(final_info, index)
        infos['final_info'] = terminal_infos
        infos['final_observation'] = infos.pop('final_obs')
        infos['_final_observation'] = infos.pop('_final_obs')

    return observations, rewards, costs, terminated, truncated, infos


class SafetyVectorRender:
    """Retain tiled rendering for Gymnasium-backed safety vectors."""

    if TYPE_CHECKING:
        def call(self, name: str) -> tuple[np.ndarray, ...]: ...

    def get_images(self) -> list[np.ndarray]:
        """Return one rendered image per vector member."""
        return list(self.call('render'))

    def render(self) -> Any:
        """Return the rendered images tiled into one array."""
        return tile_images(self.get_images())
