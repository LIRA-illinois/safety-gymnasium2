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
# Modified by Safety Gymnasium 2 contributors for the core release.
# ==============================================================================
"""Safety-Gymnasium Environments."""

import copy

from gymnasium import make as gymnasium_make
from gymnasium import register as gymnasium_register

from safety_gymnasium2 import vector, wrappers
from safety_gymnasium2.tasks.safe_multi_agent.tasks.velocity.safe_mujoco_multi import make_ma
from safety_gymnasium2.utils.registration import make, register
from safety_gymnasium2.version import __version__


__all__ = [
    'gymnasium_make',
    'gymnasium_register',
    'make',
    'register',
]

VERSION = 'v0'
ROBOT_NAMES = ('Point', 'Car', 'Doggo', 'Racecar', 'Ant')
MAKE_DEBUG_ENVIRONMENTS = True

# ========================================
# Helper Methods for Easy Registration
# ========================================

PREFIX = 'Safety'

robots = ROBOT_NAMES


def __register_helper(env_id, entry_point, spec_kwargs=None, *, gymnasium_alias=True, **kwargs):
    """Register a native environment and optionally a single-agent Gymnasium alias."""
    if spec_kwargs is None:
        spec_kwargs = {}

    register(
        id=env_id,
        entry_point=entry_point,
        kwargs=spec_kwargs,
        **kwargs,
    )
    if gymnasium_alias:
        env_name, dash, version = env_id.partition('-')
        gymnasium_register(
            id=f'SafetyGymnasium2/{env_name}Gymnasium{dash}{version}',
            entry_point='safety_gymnasium2.wrappers.gymnasium_conversion:make_gymnasium_environment',
            kwargs={'env_id': env_id},
            **kwargs,
        )


def __combine(tasks, agents, max_episode_steps):
    """Combine tasks and agents together to register environment tasks."""
    for task_name, task_config in tasks.items():
        # Vector inputs
        for robot_name in agents:
            env_id = f'{PREFIX}{robot_name}{task_name}-{VERSION}'
            combined_config = copy.deepcopy(task_config)
            combined_config.update({'agent_name': robot_name})

            __register_helper(
                env_id=env_id,
                entry_point='safety_gymnasium2.builder:Builder',
                spec_kwargs={'config': combined_config, 'task_id': env_id},
                max_episode_steps=max_episode_steps,
            )

            if MAKE_DEBUG_ENVIRONMENTS and robot_name in ['Point', 'Car', 'Racecar']:
                # Keyboard inputs for debugging
                debug_env_name = f'{PREFIX}{robot_name}{task_name}Debug-{VERSION}'
                debug_config = {'debug': True}
                debug_config.update(combined_config)
                __register_helper(
                    env_id=debug_env_name,
                    entry_point='safety_gymnasium2.builder:Builder',
                    spec_kwargs={'config': debug_config, 'task_id': env_id},
                    max_episode_steps=max_episode_steps,
                )


# ----------------------------------------
# Safety Navigation
# ----------------------------------------

# Button Environments
# ----------------------------------------
button_tasks = {
    'ButtonBase': {'task_name': 'ButtonBase'},
    'Button0': {},
    'Button1': {},
    'Button2': {},
}
__combine(button_tasks, robots, max_episode_steps=1000)


# Push Environments
# ----------------------------------------
push_tasks = {'PushBase': {'task_name': 'PushBase'}, 'Push0': {}, 'Push1': {}, 'Push2': {}}
__combine(push_tasks, robots, max_episode_steps=1000)


# Goal Environments
# ----------------------------------------
goal_tasks = {'GoalBase': {'task_name': 'GoalBase'}, 'Goal0': {}, 'Goal1': {}, 'Goal2': {}}
__combine(goal_tasks, robots, max_episode_steps=1000)


# Circle Environments
# ----------------------------------------
circle_tasks = {
    'CircleBase': {'task_name': 'CircleBase'},
    'Circle0': {},
    'Circle1': {},
    'Circle2': {},
}
__combine(circle_tasks, robots, max_episode_steps=500)


# Run Environments
# ----------------------------------------
run_tasks = {'RunBase': {'task_name': 'RunBase'}, 'Run0': {}}
__combine(run_tasks, robots, max_episode_steps=500)


# Fading Environments
# ----------------------------------------
fading_tasks = {'FadingEasy0': {}, 'FadingEasy1': {}, 'FadingEasy2': {}}
__combine(fading_tasks, robots, max_episode_steps=1000)

fading_tasks = {'FadingHard0': {}, 'FadingHard1': {}, 'FadingHard2': {}}
__combine(fading_tasks, robots, max_episode_steps=1000)


# ----------------------------------------
# Safety Velocity
# ----------------------------------------

__register_helper(
    env_id='SafetyHalfCheetahVelocity-v0',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_half_cheetah_velocity_v0:SafetyHalfCheetahVelocityEnv',
    max_episode_steps=1000,
    reward_threshold=4800.0,
)

__register_helper(
    env_id='SafetyHopperVelocity-v0',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_hopper_velocity_v0:SafetyHopperVelocityEnv',
    max_episode_steps=1000,
    reward_threshold=3800.0,
)

__register_helper(
    env_id='SafetySwimmerVelocity-v0',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_swimmer_velocity_v0:SafetySwimmerVelocityEnv',
    max_episode_steps=1000,
    reward_threshold=360.0,
)

__register_helper(
    env_id='SafetyWalker2dVelocity-v0',
    max_episode_steps=1000,
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_walker2d_velocity_v0:SafetyWalker2dVelocityEnv',
)

__register_helper(
    env_id='SafetyAntVelocity-v0',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_ant_velocity_v0:SafetyAntVelocityEnv',
    max_episode_steps=1000,
    reward_threshold=6000.0,
)

__register_helper(
    env_id='SafetyHumanoidVelocity-v0',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_humanoid_velocity_v0:SafetyHumanoidVelocityEnv',
    max_episode_steps=1000,
)

__register_helper(
    env_id='SafetyHalfCheetahVelocity-v1',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_half_cheetah_velocity_v1:SafetyHalfCheetahVelocityEnv',
    max_episode_steps=1000,
    reward_threshold=4800.0,
)

__register_helper(
    env_id='SafetyHopperVelocity-v1',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_hopper_velocity_v1:SafetyHopperVelocityEnv',
    max_episode_steps=1000,
    reward_threshold=3800.0,
)

__register_helper(
    env_id='SafetySwimmerVelocity-v1',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_swimmer_velocity_v1:SafetySwimmerVelocityEnv',
    max_episode_steps=1000,
    reward_threshold=360.0,
)

__register_helper(
    env_id='SafetyWalker2dVelocity-v1',
    max_episode_steps=1000,
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_walker2d_velocity_v1:SafetyWalker2dVelocityEnv',
)

__register_helper(
    env_id='SafetyAntVelocity-v1',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_ant_velocity_v1:SafetyAntVelocityEnv',
    max_episode_steps=1000,
    reward_threshold=6000.0,
)

__register_helper(
    env_id='SafetyHumanoidVelocity-v1',
    entry_point='safety_gymnasium2.tasks.safe_velocity.safety_humanoid_velocity_v1:SafetyHumanoidVelocityEnv',
    max_episode_steps=1000,
)


for velocity_robot in ('HalfCheetah', 'Hopper', 'Swimmer', 'Walker2d', 'Ant', 'Humanoid'):
    __register_helper(
        env_id=f'Safety{velocity_robot}Velocity-v2',
        entry_point=(
            'safety_gymnasium2.tasks.safe_velocity.safety_velocity_v2:'
            f'Safety{velocity_robot}VelocityEnv'
        ),
        max_episode_steps=1000,
    )


def __combine_multi(tasks, agents, max_episode_steps):
    """Combine tasks and agents together to register environment tasks."""
    for task_name, task_config in tasks.items():
        # Vector inputs
        for robot_name in agents:
            env_id = f'{PREFIX}{robot_name}{task_name}-{VERSION}'
            combined_config = copy.deepcopy(task_config)
            combined_config.update({'agent_name': robot_name})

            __register_helper(
                env_id=env_id,
                entry_point='safety_gymnasium2.tasks.safe_multi_agent.builder:Builder',
                spec_kwargs={'config': combined_config, 'task_id': env_id},
                max_episode_steps=max_episode_steps,
                disable_env_checker=True,
                gymnasium_alias=False,
            )

            if MAKE_DEBUG_ENVIRONMENTS and robot_name in ['Point', 'Car', 'Racecar']:
                # Keyboard inputs for debugging
                debug_env_name = f'{PREFIX}{robot_name}{task_name}Debug-{VERSION}'
                debug_config = {'debug': True}
                debug_config.update(combined_config)
                __register_helper(
                    env_id=debug_env_name,
                    entry_point='safety_gymnasium2.tasks.safe_multi_agent.builder:Builder',
                    spec_kwargs={'config': debug_config, 'task_id': env_id},
                    max_episode_steps=max_episode_steps,
                    disable_env_checker=True,
                    gymnasium_alias=False,
                )


# ----------------------------------------
# Safety Multi-Agent
# ----------------------------------------

# Multi Goal Environments
# ----------------------------------------
multi_goal_tasks = {'MultiGoal0': {}, 'MultiGoal1': {}, 'MultiGoal2': {}}
__combine_multi(multi_goal_tasks, ('Point', 'Ant'), max_episode_steps=1000)
