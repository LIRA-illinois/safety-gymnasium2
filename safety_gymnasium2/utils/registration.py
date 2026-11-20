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
"""Register and make native Safety Gymnasium environments."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from importlib import import_module
from typing import TYPE_CHECKING, Any, cast

from gymnasium import Env, Wrapper, error, logger
from gymnasium.envs.registration import EnvSpec, load_env_creator
from gymnasium.wrappers import HumanRendering, OrderEnforcing, RenderCollection

from safety_gymnasium2.wrappers import SafeAutoResetWrapper, SafePassiveEnvChecker, SafeTimeLimit

if TYPE_CHECKING:
    from safety_gymnasium2.builder import Builder
    from safety_gymnasium2.tasks.safe_multi_agent.builder import Builder as MultiAgentBuilder


safe_registry: dict[str, EnvSpec] = {}
_autoreset_by_id: dict[str, bool] = {}
_multi_agent_builder = 'safety_gymnasium2.tasks.safe_multi_agent.builder:Builder'
_builder_entry_points = ('safety_gymnasium2.builder:Builder', _multi_agent_builder)


class _SafeHumanRendering(HumanRendering):
    """Display a frame and forward the full native step result."""

    def step(self, action: Any) -> Any:
        result = self.env.step(action)
        self._render_frame()
        return result


class _MultiAgentAttributes(Wrapper):
    """Expose the parallel agent attributes through the native wrapper stack."""

    @property
    def agents(self) -> list[str]:
        return cast('MultiAgentBuilder', self.unwrapped).agents

    @property
    def possible_agents(self) -> list[str]:
        return cast('MultiAgentBuilder', self.unwrapped).possible_agents

    @property
    def num_agents(self) -> int:
        return cast('MultiAgentBuilder', self.unwrapped).num_agents

    @property
    def spec(self) -> EnvSpec | None:
        return self.env.spec


def register(id: str, *, autoreset: bool = False, **kwargs: Any) -> None:
    """Register a native environment with the six-value step API."""
    if id in safe_registry:
        logger.warn(f'Overriding native environment {id} already in registry.')
    safe_registry[id] = EnvSpec(id=id, **kwargs)
    _autoreset_by_id[id] = autoreset


def spec(id: str) -> EnvSpec:
    """Return the registered native environment spec."""
    if ':' in id:
        module_name, id = id.split(':', maxsplit=1)
        import_module(module_name)
    try:
        return safe_registry[id]
    except KeyError as exc:
        raise error.NameNotFound(
            f'Environment {id!r} is not registered in Safety Gymnasium 2.'
        ) from exc


def _environment_kwargs(env_spec: EnvSpec, overrides: Mapping[str, Any]) -> dict[str, Any]:
    env_kwargs = deepcopy(env_spec.kwargs)
    for key, value in overrides.items():
        if not isinstance(value, Mapping) or not isinstance(env_kwargs.get(key), Mapping):
            env_kwargs[key] = value
            continue
        if key == 'config' and any(
            name in env_kwargs[key] and name in value and value[name] != env_kwargs[key][name]
            for name in ('agent_name', 'task_name')
        ):
            raise ValueError(f'The config agent and task must match environment {env_spec.id!r}.')
        env_kwargs[key] = {**env_kwargs[key], **value}
    if env_spec.entry_point in _builder_entry_points:
        # The factory applies the registered horizon outside the Builder.
        env_kwargs['use_task_time_limit'] = False
    return env_kwargs


def _create_environment(
    env_spec: EnvSpec,
    overrides: Mapping[str, Any],
) -> tuple[Env, type[HumanRendering | RenderCollection] | None]:
    """Construct a native base environment and select any render wrapper."""
    creator = env_spec.entry_point
    if creator is None:
        raise error.Error(f'Environment {env_spec.id!r} has no entry point.')
    if isinstance(creator, str):
        creator = load_env_creator(creator)

    render_modes = getattr(creator, 'metadata', {}).get('render_modes')
    env_kwargs = _environment_kwargs(env_spec, overrides)
    render_mode = env_kwargs.get('render_mode')
    render_wrapper = None
    if render_mode is not None and render_modes is not None and render_mode not in render_modes:
        if render_mode == 'human' and (
            'rgb_array' in render_modes or 'rgb_array_list' in render_modes
        ):
            env_kwargs['render_mode'] = (
                'rgb_array' if 'rgb_array' in render_modes else 'rgb_array_list'
            )
            render_wrapper = _SafeHumanRendering
        elif render_mode.endswith('_list') and render_mode.removesuffix('_list') in render_modes:
            env_kwargs['render_mode'] = render_mode.removesuffix('_list')
            render_wrapper = RenderCollection
        else:
            logger.warn(
                f'Render mode {render_mode!r} is not in the supported modes {render_modes}.'
            )

    env = creator(**env_kwargs)
    if not isinstance(env, Env):
        raise TypeError(f'Environment {env_spec.id!r} must inherit from gymnasium.Env.')
    env.unwrapped.spec = EnvSpec(
        id=env_spec.id,
        entry_point=env_spec.entry_point,
        reward_threshold=env_spec.reward_threshold,
        nondeterministic=env_spec.nondeterministic,
        order_enforce=False,
        disable_env_checker=True,
        kwargs=env_kwargs,
        vector_entry_point=env_spec.vector_entry_point,
    )
    return env, render_wrapper


def make(
    id: str | EnvSpec,
    max_episode_steps: int | None = None,
    autoreset: bool | None = None,
    apply_api_compatibility: bool | None = None,
    disable_env_checker: bool | None = None,
    **kwargs: Any,
) -> Env:
    """Create a native Safety Gymnasium environment.

    Args:
        id: Registered environment ID or a Gymnasium environment specification.
        max_episode_steps: Override the registered horizon, or pass -1 to disable it.
        autoreset: Reset on the same step that an episode ends.
        apply_api_compatibility: Legacy option. The old step API is unsupported.
        disable_env_checker: Override the registered passive checker setting.
        **kwargs: Override the registered environment constructor arguments.

    Returns:
        An environment whose step returns observation, reward, cost, termination,
        truncation, and info.
    """
    if apply_api_compatibility:
        raise ValueError('The legacy step compatibility wrapper was removed in Gymnasium 1.0.')
    env_spec = id if isinstance(id, EnvSpec) else spec(id)
    env, render_wrapper = _create_environment(env_spec, kwargs)

    base_spec = env.spec
    if base_spec is None:
        raise error.Error(f'Environment {env_spec.id!r} did not retain its specification.')
    prior_wrappers = base_spec.additional_wrappers
    if env_spec.additional_wrappers[: len(prior_wrappers)] != prior_wrappers:
        raise ValueError(f'Pre-wrapped environment does not match the spec for {env_spec.id!r}.')

    disable_checker = (
        env_spec.disable_env_checker if disable_env_checker is None else disable_env_checker
    )
    if not disable_checker:
        env = SafePassiveEnvChecker(env)
    if env_spec.order_enforce:
        env = OrderEnforcing(env)

    if max_episode_steps is None:
        max_episode_steps = env_spec.max_episode_steps
        if env_spec.entry_point in _builder_entry_points:
            builder = cast('Builder | MultiAgentBuilder', env.unwrapped)
            task_steps = builder.task.num_steps
            max_episode_steps = (
                task_steps
                if max_episode_steps is None
                else min(
                    task_steps,
                    max_episode_steps,
                )
            )
    if max_episode_steps is not None and max_episode_steps != -1:
        env = SafeTimeLimit(env, max_episode_steps)
    if autoreset or (autoreset is None and _autoreset_by_id.get(env_spec.id, False)):
        env = SafeAutoResetWrapper(env)

    for wrapper_spec in env_spec.additional_wrappers[len(prior_wrappers) :]:
        if wrapper_spec.kwargs is None:
            raise ValueError(
                f'Wrapper {wrapper_spec.name!r} does not record its constructor arguments.'
            )
        wrapper = load_env_creator(wrapper_spec.entry_point)
        wrapped = wrapper(env=env, **wrapper_spec.kwargs)
        if not isinstance(wrapped, Env):
            raise TypeError(f'Wrapper {wrapper_spec.name!r} must inherit from gymnasium.Env.')
        env = wrapped

    if render_wrapper is not None:
        env = render_wrapper(env)
    if env_spec.entry_point == _multi_agent_builder:
        env = _MultiAgentAttributes(env)
    return env
