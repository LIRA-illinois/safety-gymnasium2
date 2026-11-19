"""Headless examples for collecting single and vector safety transitions."""

from contextlib import closing

import numpy as np
import safety_gymnasium2 as sg2


def single_environment() -> None:
    """Step a native safety environment and reset between episodes."""
    with closing(sg2.make('SafetyPointGoal0-v0', max_episode_steps=2)) as env:
        observation, _ = env.reset(seed=42)
        env.action_space.seed(42)
        for _ in range(4):
            action = env.action_space.sample()
            observation, reward, cost, terminated, truncated, _ = env.step(action)  # ty: ignore[invalid-assignment]
            print('Observation shape', observation.shape, 'reward', reward, 'cost', cost)
            if terminated or truncated:
                observation, _ = env.reset()


def vector_environments() -> None:
    """Collect transitions from two lanes with same-step autoreset."""
    env = sg2.vector.make(
        'SafetyPointGoal0-v0',
        num_envs=2,
        asynchronous=False,
        max_episode_steps=2,
    )
    with closing(env):
        observations, _ = env.reset(seed=42)
        env.action_space.seed(42)
        for _ in range(4):
            actions = env.action_space.sample()
            next_obs, rewards, costs, terminated, truncated, info = env.step(actions)  # ty: ignore[invalid-assignment]
            finished = np.logical_or(terminated, truncated)
            transition_next_obs = next_obs.copy()
            if '_final_observation' in info:
                mask = info['_final_observation']
                transition_next_obs[mask] = np.stack(info['final_observation'][mask])

            # Store transition_next_obs in replay and use next_obs for the next action.
            print(
                'Transition batch',
                observations.shape,
                'to',
                transition_next_obs.shape,
                'finished lanes',
                np.flatnonzero(finished),
                'reward',
                rewards,
                'cost',
                costs,
            )
            observations = next_obs


if __name__ == '__main__':
    single_environment()
    vector_environments()
