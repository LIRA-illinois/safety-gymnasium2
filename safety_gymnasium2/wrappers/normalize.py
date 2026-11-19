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
"""Normalize observations, rewards, and costs for native safety transitions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self, cast

import gymnasium as gym
import numpy as np
from gymnasium.vector import VectorEnv, VectorWrapper
from gymnasium.vector.utils import batch_space
from gymnasium.wrappers.utils import RunningMeanStd

if TYPE_CHECKING:
    from safety_gymnasium2.utils._types import NativeStep


class _ObservationNormalization:
    """Running observation statistics shared by both wrapper interfaces."""

    env: gym.Env | VectorEnv

    def _init_normalization(
        self,
        single_space: gym.Space,
        epsilon: float,
        num_envs: int | None = None,
    ) -> None:
        if not isinstance(single_space, gym.spaces.Box):
            raise TypeError('SafeNormalizeObservation requires a Box observation space.')
        normalized_space = gym.spaces.Box(
            -np.inf, np.inf, shape=single_space.shape, dtype=np.float64,
        )
        if num_envs is None:
            self.observation_space = normalized_space
        else:
            self.single_observation_space = normalized_space
            self.observation_space = batch_space(normalized_space, num_envs)
        self.is_vector_env = num_envs is not None
        self.obs_rms = RunningMeanStd(shape=single_space.shape)
        self.epsilon = epsilon
        self.update_running_mean = True

    def normalize(self, observations: np.ndarray) -> np.ndarray:
        """Scale a batch of observations using the running mean and variance."""
        if self.update_running_mean:
            self.obs_rms.update(observations)
        return (observations - self.obs_rms.mean) / np.sqrt(self.obs_rms.var + self.epsilon)

    def _normalize_observation(self, observation: np.ndarray) -> np.ndarray:
        if self.is_vector_env:
            return self.normalize(observation)
        return self.normalize(np.expand_dims(observation, axis=0))[0]

    def reset(self, **kwargs):
        """Reset the environment and normalize its observation."""
        observation, info = self.env.reset(**kwargs)
        return self._normalize_observation(observation), info

    def _normalize_final(self, final: np.ndarray, mask: np.ndarray) -> np.ndarray:
        indices = np.flatnonzero(mask)
        normalized = final.copy()
        if not len(indices):
            return normalized
        batch = self.normalize(np.stack(final[mask]))
        for index, item in zip(indices, batch, strict=True):
            normalized[index] = item
        return normalized

    def _step(self, action: Any) -> NativeStep:
        result = cast('NativeStep', self.env.step(action))
        observation, reward, cost, terminated, truncated, info = result
        observation = self._normalize_observation(observation)
        if 'final_observation' in info:
            final = info['final_observation']
            normalized = (
                self._normalize_final(final, info['_final_observation'])
                if self.is_vector_env
                else self._normalize_observation(final)
            )
            info = {**info, 'original_final_observation': final, 'final_observation': normalized}
        return observation, reward, cost, terminated, truncated, info


class _VectorNormalizeObservation(_ObservationNormalization, VectorWrapper):
    def __init__(self, env: VectorEnv, epsilon: float) -> None:
        VectorWrapper.__init__(self, env)
        self._init_normalization(env.single_observation_space, epsilon, env.num_envs)

    def step(self, actions: Any) -> Any:
        """Normalize observations for a batch of safety transitions."""
        return self._step(actions)


class SafeNormalizeObservation(
    _ObservationNormalization, gym.Wrapper, gym.utils.RecordConstructorArgs,
):
    """Normalize observations in a native single or vector environment."""

    def __new__(cls, env: gym.Env | VectorEnv, epsilon: float = 1e-8) -> Self | _VectorNormalizeObservation:
        if isinstance(env, VectorEnv):
            return _VectorNormalizeObservation(env, epsilon)
        return super().__new__(cls)

    def __init__(self, env: gym.Env, epsilon: float = 1e-8) -> None:
        gym.utils.RecordConstructorArgs.__init__(self, epsilon=epsilon)
        gym.Wrapper.__init__(self, env)
        self._init_normalization(env.observation_space, epsilon)

    def step(self, action: Any) -> Any:
        """Normalize the observation in a safety transition."""
        return self._step(action)


class _ReturnNormalization:
    """Running discounted statistics for a reward or a cost."""

    env: gym.Env | VectorEnv
    _normalize_reward: bool

    def _init_normalization(
        self,
        gamma: float,
        epsilon: float,
        num_envs: int | None = None,
    ) -> None:
        self.is_vector_env = num_envs is not None
        self.returns = np.zeros(1 if num_envs is None else num_envs)
        self.return_rms = RunningMeanStd(shape=())
        self.gamma = gamma
        self.epsilon = epsilon
        self.update_running_mean = True

    def normalize(self, values: np.ndarray) -> np.ndarray:
        """Scale immediate values by the running variance of discounted returns."""
        if self.update_running_mean:
            self.return_rms.update(self.returns)
        return values / np.sqrt(self.return_rms.var + self.epsilon)

    def _step(self, action: Any) -> NativeStep:
        result = cast('NativeStep', self.env.step(action))
        obs, reward, cost, terminated, truncated, info = result
        values = np.asarray(reward if self._normalize_reward else cost)
        self.returns = self.returns * self.gamma * (1 - np.asarray(terminated)) + values
        normalized = self.normalize(values)
        if not self.is_vector_env:
            normalized = float(normalized)
        if self._normalize_reward:
            reward = normalized
        else:
            cost = normalized
        return obs, reward, cost, terminated, truncated, info


class _VectorNormalizeReturn(_ReturnNormalization, VectorWrapper):
    def __init__(
        self,
        env: VectorEnv,
        gamma: float,
        epsilon: float,
        normalize_reward: bool,
    ) -> None:
        VectorWrapper.__init__(self, env)
        self._normalize_reward = normalize_reward
        self._init_normalization(gamma, epsilon, env.num_envs)

    def step(self, actions: Any) -> Any:
        """Normalize one component of the batched safety transition."""
        return self._step(actions)


class _NormalizeReturn(_ReturnNormalization, gym.Wrapper, gym.utils.RecordConstructorArgs):
    def __new__(
        cls, env: gym.Env | VectorEnv, gamma: float = 0.99, epsilon: float = 1e-8,
    ) -> Self | _VectorNormalizeReturn:
        if isinstance(env, VectorEnv):
            return _VectorNormalizeReturn(env, gamma, epsilon, cls._normalize_reward)
        return super().__new__(cls)

    def __init__(self, env: gym.Env, gamma: float = 0.99, epsilon: float = 1e-8) -> None:
        gym.utils.RecordConstructorArgs.__init__(self, gamma=gamma, epsilon=epsilon)
        gym.Wrapper.__init__(self, env)
        self._init_normalization(gamma, epsilon)

    def step(self, action: Any) -> Any:
        """Normalize one component of the safety transition."""
        return self._step(action)


class SafeNormalizeReward(_NormalizeReturn):
    """Normalize rewards in a native single or vector environment."""

    _normalize_reward = True


class SafeNormalizeCost(_NormalizeReturn):
    """Normalize costs in a native single or vector environment."""

    _normalize_reward = False
