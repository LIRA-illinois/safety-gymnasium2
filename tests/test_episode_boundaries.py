from __future__ import annotations

from collections.abc import Mapping
from functools import partial
from typing import TYPE_CHECKING, Any, cast

import gymnasium as gym
import numpy as np
import safety_gymnasium2 as sg2
from absl.testing import absltest, parameterized
from gymnasium.utils.env_checker import check_env
from safety_gymnasium2.utils import registration
from safety_gymnasium2.vector import SafetyAsyncVectorEnv, SafetySyncVectorEnv
from safety_gymnasium2.wrappers import (
    SafeAutoResetWrapper,
    SafeNormalizeCost,
    SafeNormalizeReward,
)

if TYPE_CHECKING:
    from gymnasium.envs.registration import EnvSpec
    from safety_gymnasium2.utils._types import NativeStep
    from safety_gymnasium2.wrappers.gymnasium_conversion import _RegisteredGymnasiumAlias

_NATIVE_ID = 'SafetyBoundaryTest-v0'
_ALIAS_ID = 'SafetyGymnasium2/SafetyPointGoal0Gymnasium-v0'


class _BoundaryEnv(gym.Env):
    """A native environment with distinguishable reset and terminal observations."""

    observation_space = gym.spaces.Box(0.0, 1000.0, (1,), dtype=np.float64)
    action_space = gym.spaces.Discrete(2)

    def __init__(self, end_after: int = 2, truncate: bool = False) -> None:
        self._end_after = end_after
        self._truncate = truncate
        self._reset_count = 0
        self._step_count = 0

    def reset(
        self,
        *,
        seed: int | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        super().reset(seed=seed)
        self._step_count = 0
        self._reset_count += 1
        return np.array([self._reset_count], dtype=np.float64), {}

    def step(self, action: int) -> NativeStep:  # ty: ignore[incompatible-method-override]
        self._step_count += 1
        finished = self._step_count == self._end_after
        return (
            np.array([10.0 * self._step_count]),
            1.0,
            2.0,
            finished and not self._truncate,
            finished and self._truncate,
            {'steps': self._step_count},
        )


def _wrapped_boundary_env() -> gym.Env:
    return gym.Wrapper(SafeAutoResetWrapper(_BoundaryEnv()))


class VectorEpisodeTest(parameterized.TestCase):
    @parameterized.named_parameters(('sync', False, None), ('spawn', True, 'spawn'))
    def test_registered_autoreset_is_disabled_inside_vectors(
        self,
        asynchronous: bool,
        context: str | None,
    ) -> None:
        sg2.register(_NATIVE_ID, entry_point=partial(_BoundaryEnv, 1), autoreset=True)
        self.addCleanup(registration.safe_registry.pop, _NATIVE_ID)
        self.addCleanup(registration._autoreset_by_id.pop, _NATIVE_ID)
        env = sg2.vector.make(
            _NATIVE_ID,
            num_envs=2,
            asynchronous=asynchronous,
            multiprocessing_context=context,
        )
        self.addCleanup(env.close)
        env.reset(seed=3)

        observation, _, cost, _, _, info = cast('NativeStep', env.step(np.zeros(2, dtype=int)))

        np.testing.assert_array_equal(observation, [[2.0], [2.0]])
        np.testing.assert_array_equal(np.stack(info['final_observation']), [[10.0], [10.0]])
        self.assertEqual(
            (cost.tolist(), info['final_info'].tolist(), info['_final_observation'].tolist()),
            ([2.0, 2.0], [{'steps': 1}, {'steps': 1}], [True, True]),
        )

    @parameterized.named_parameters(
        ('sync', SafetySyncVectorEnv),
        ('spawn', partial(SafetyAsyncVectorEnv, context='spawn')),
    )
    def test_vector_rejects_nested_native_autoreset(self, vectorize: Any) -> None:
        with self.assertRaisesRegex(ValueError, 'cannot use SafeAutoResetWrapper'):
            vectorize([_wrapped_boundary_env])


class ReturnNormalizationTest(parameterized.TestCase):
    @parameterized.product(
        normalize=[SafeNormalizeReward, SafeNormalizeCost],
        truncate=[False, True],
    )
    def test_final_transition_is_counted_and_next_episode_starts_clean(
        self,
        normalize: type[SafeNormalizeReward | SafeNormalizeCost],
        truncate: bool,
    ) -> None:
        immediate = 1.0 if normalize is SafeNormalizeReward else 2.0
        env = normalize(SafeAutoResetWrapper(_BoundaryEnv(truncate=truncate)), gamma=0.5)
        self.addCleanup(env.close)
        env.reset()
        prior_count = env.return_rms.count

        env.step(0)
        env.step(0)

        np.testing.assert_array_equal(env.returns, [0.0])
        self.assertAlmostEqual(env.return_rms.mean, immediate * 2.5 / (prior_count + 2))
        env.step(0)
        np.testing.assert_array_equal(env.returns, [immediate])

    @parameterized.named_parameters(('reward', SafeNormalizeReward), ('cost', SafeNormalizeCost))
    def test_explicit_single_reset_leaves_running_statistics(
        self,
        normalize: type[SafeNormalizeReward | SafeNormalizeCost],
    ) -> None:
        env = normalize(_BoundaryEnv())
        self.addCleanup(env.close)
        env.reset()
        env.step(0)
        previous_count = env.return_rms.count
        env.reset()

        np.testing.assert_array_equal(env.returns, [0.0])
        self.assertEqual(env.return_rms.count, previous_count)

    @parameterized.product(
        normalize=[SafeNormalizeReward, SafeNormalizeCost],
        truncate=[False, True],
    )
    def test_vector_normalization_clears_only_finished_or_explicitly_reset_lanes(
        self,
        normalize: type[SafeNormalizeReward | SafeNormalizeCost],
        truncate: bool,
    ) -> None:
        immediate = 1.0 if normalize is SafeNormalizeReward else 2.0
        vector_env = SafetySyncVectorEnv(
            [partial(_BoundaryEnv, 2, truncate), partial(_BoundaryEnv, 5)]
        )
        env = normalize(vector_env, gamma=0.5)
        self.addCleanup(env.close)
        env.reset()
        actions = np.zeros(2, dtype=int)
        env.step(actions)
        env.step(actions)
        np.testing.assert_array_equal(env.returns, [0.0, immediate * 1.5])
        env.step(actions)
        self.assertEqual(env.returns[0], immediate)

        env.reset(options={'reset_mask': np.array([True, False])})

        np.testing.assert_array_equal(env.returns, [0.0, immediate * 1.75])


class GymnasiumAliasTest(parameterized.TestCase):
    def test_unwrapped_alias_matches_gymnasium_and_native_access_is_explicit(self) -> None:
        env = gym.make(_ALIAS_ID)
        self.addCleanup(env.close)
        unwrapped = cast('_RegisteredGymnasiumAlias', env.unwrapped)
        check_env(unwrapped, skip_render_check=True)
        unwrapped.reset(seed=3)
        native = unwrapped.native_env
        native.reset(seed=3)
        action = np.zeros(2)

        self.assertLen(native.step(action), 6)
        self.assertIn('cost', unwrapped.step(action)[4])

    def test_alias_spec_recreates_explicit_horizon(self) -> None:
        env = gym.make(_ALIAS_ID, max_episode_steps=1)
        self.addCleanup(env.close)
        recreated = cast('EnvSpec', env.spec).make()
        self.addCleanup(recreated.close)
        recreated.reset(seed=3)

        self.assertEqual(cast('EnvSpec', recreated.spec).id, _ALIAS_ID)
        self.assertTrue(recreated.step(np.zeros(2))[3])

    def test_alias_default_and_disabled_horizons(self) -> None:
        default = gym.make(_ALIAS_ID)
        self.addCleanup(default.close)
        unlimited = gym.make(_ALIAS_ID, max_episode_steps=-1)
        self.addCleanup(unlimited.close)

        self.assertEqual(cast('EnvSpec', default.spec).max_episode_steps, 1_000)
        self.assertIsNone(cast('EnvSpec', unlimited.spec).max_episode_steps)

    def test_alias_rejects_native_horizon_configuration(self) -> None:
        with self.assertRaisesRegex(ValueError, 'max_episode_steps'):
            gym.make(_ALIAS_ID, config={'num_steps': 1})

    def test_gymnasium_make_vec_keeps_five_value_aliases(self) -> None:
        env = gym.make_vec(_ALIAS_ID, num_envs=2, vectorization_mode='sync')
        self.addCleanup(env.close)
        env.reset(seed=3)
        result = env.step(np.zeros((2, 2)))

        self.assertLen(result, 5)
        np.testing.assert_array_equal(result[4]['cost'], [0.0, 0.0])


if __name__ == '__main__':
    absltest.main()
