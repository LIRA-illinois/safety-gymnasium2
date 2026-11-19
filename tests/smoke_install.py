"""Verify local builds and smoke-test their installed environments."""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import sys
import tarfile
import zipfile
from itertools import product
from pathlib import Path

_DISTRIBUTIONS = (
    'safety_gymnasium2',
    'safety_gymnasium2_building_scenery',
    'safety_gymnasium2_building_structure',
    'safety_gymnasium2_racing_assets',
)
_ARCHIVE_LIMIT = 100_000_000


def check_archives(directory: Path) -> None:
    """Verify one wheel and one source archive per workspace member."""
    for distribution, suffix in product(_DISTRIBUTIONS, ('.whl', '.tar.gz')):
        paths = list(directory.glob(f'{distribution}-*{suffix}'))
        assert len(paths) == 1, f'Expected one {distribution} {suffix}, found {paths}'
        path = paths[0]
        size = path.stat().st_size
        assert size < _ARCHIVE_LIMIT, f'{path.name} is {size} bytes'
        if suffix == '.whl':
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
        else:
            with tarfile.open(path) as archive:
                names = archive.getnames()
        for name in names:
            assert {'legacy', 'safe_isaac_gym', 'safe_vla'}.isdisjoint(Path(name).parts), name
        print(f'{path.name}: {size:,} bytes')


def smoke_install(extra: str) -> None:
    """Exercise the installed core or one independent asset extra."""
    import gymnasium as gym
    import safety_gymnasium2 as sg2

    assert sg2.__version__ == importlib.metadata.version('safety-gymnasium2')
    assert Path(sg2.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    assert importlib.util.find_spec('safety_gymnasium2.tasks.safe_isaac_gym') is None
    assert importlib.util.find_spec('safety_gymnasium2.tasks.safe_vla') is None

    for required, env_id in (
        ('racing', 'SafetyRacecarRace0-v0'),
        ('building', 'SafetyPointBuildingGoal0-v0'),
    ):
        if extra == required:
            continue
        try:
            with sg2.make(env_id):
                raise AssertionError(f'{env_id} loaded without the {required} extra')
        except ImportError as error:
            assert f'safety-gymnasium2[{required}]' in str(error), str(error)

    tasks_by_extra = {
        'core': ('SafetyPointGoal0-v0', 'SafetyRacecarGoal0-v0', 'SafetyPointGoal0Vision-v0'),
        'racing': ('SafetyRacecarRace0-v0', 'SafetyRacecarFormulaOne0-v0'),
        'building': ('SafetyPointBuildingGoal0-v0', 'SafetyPointBuildingPush0-v0'),
    }
    for env_id in tasks_by_extra[extra]:
        vision = 'Vision' in env_id
        config = {'vision_env_conf.vision_size': (48, 32)} if vision else {}
        with sg2.make(
            env_id,
            config=config,
            render_mode=None if vision else 'rgb_array',
            width=48,
            height=32,
            max_episode_steps=1,
        ) as env:
            observation, _ = env.reset(seed=17)
            assert env.observation_space.contains(observation), env_id
            transition = env.step(env.action_space.sample())
            assert len(transition) == 6 and transition[4], env_id
            frame = observation['vision'] if vision else env.render()
            assert frame.shape == (32, 48, 3), env_id

    if extra == 'core':
        with gym.make('SafetyGymnasium2/SafetyPointGoal0Gymnasium-v0', max_episode_steps=1) as env:
            env.reset(seed=17)
            _, _, _, truncated, info = env.step(env.action_space.sample())
            assert truncated and 'cost' in info
        with sg2.make('SafetyHalfCheetahVelocity-v2') as env:
            env.reset(seed=17)
            assert len(env.step(env.action_space.sample())) == 6
        with sg2.make('SafetyAntMultiGoal0-v0', max_episode_steps=1) as env:
            env.reset(seed=17)
            action_by_agent = {agent: env.action_space(agent).sample() for agent in env.agents}
            transition = env.step(action_by_agent)
            assert len(transition) == 6 and all(transition[4].values())

    print(f'{extra} install smoke passed')


def main() -> None:
    """Run archive validation or smoke tests for an installed extra."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('archives', 'core', 'racing', 'building'))
    parser.add_argument('--dist', type=Path, default=Path('dist'))
    args = parser.parse_args()
    if args.mode == 'archives':
        check_archives(args.dist)
    else:
        smoke_install(args.mode)


if __name__ == '__main__':
    main()
