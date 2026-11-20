<!-- Modified for Safety Gymnasium 2. -->
# Safety Gymnasium 2

Safety Gymnasium 2 is the independent LIRA research fork of Safety Gymnasium for safe reinforcement learning. It provides MuJoCo environments with an explicit safety cost.

[Documentation](https://tran.aerospace.illinois.edu/safety-gymnasium2/) · [Environment reference](https://tran.aerospace.illinois.edu/safety-gymnasium2/environments/safe_navigation.html) · [Issue tracker](https://github.com/LIRA-illinois/safety-gymnasium2/issues)

## Why Safety-Gymnasium2?

The original Safety Gymnasium core uses exact pins for Gymnasium, Gymnasium-Robotics, and MuJoCo. The fork updates that stack, adds ranged dependencies with a `uv` lockfile for development, and tests the supported Python and simulator versions in CI.

| Project | Python | Gymnasium | Gymnasium-Robotics | MuJoCo |
| --- | --- | --- | --- | --- |
| [Original Safety Gymnasium](https://github.com/PKU-Alignment/safety-gymnasium) | 3.8+ in package metadata | 0.28.1 | 1.2.2 | 2.3.3 |
| **Safety Gymnasium 2** | **3.11+** | **1.2+** | **1.4.2+** | **4.0.1+** |

The fork retains the native six-value step API. Its namespaced single-agent aliases work with standard Gymnasium wrappers, and its vector API preserves terminal observations and costs when lanes reset on the same step.

## Environments

| Family | Released tasks | Example |
| --- | --- | --- |
| Navigation | Goal, Button, Push, Circle, Run, FadingEasy, and FadingHard with state observations | `SafetyPointGoal0-v0` |
| Velocity | HalfCheetah, Hopper, Swimmer, Walker2d, Ant, and Humanoid | `SafetyHalfCheetahVelocity-v2` |
| Multi-Agent Navigation | MultiGoal with Point or Ant | `SafetyAntMultiGoal0-v0` |
| Multi-Agent Velocity | Eight MaMuJoCo configurations available through `make_ma` | `make_ma('Ant', '2x4')` |

Single-agent navigation supports Point, Car, Racecar, Doggo, and Ant. Configuration templates such as `SafetyPointGoalBase-v0` require explicit task configuration. Keyboard debugging is available with supported Point, Car, and Racecar Debug variants such as `SafetyCarGoal2Debug-v0`.

### Benchmark versions

`Safety{Robot}Velocity-v0` and `-v1` use Gymnasium's v4 locomotion implementations. `-v2` uses upstream v5 observations, rewards, and termination with Safety Velocity v1 costs and horizons. Ant observations change from 27 to 105 values by default, and Humanoid observations change from 376 to 348. The Robotics upgrade also changes some multi-agent observation shapes. For example, Ant with `2x4` changes from 21 to 63 values per agent. See the [benchmark notes](https://github.com/LIRA-illinois/safety-gymnasium2/tree/main/benchmarks#reproducing-new-runs) for what to record with each experiment.

## Installation

Use Python 3.11 or newer. From a checkout, install the core package in an active virtual environment.

```sh
python -m pip install .
```

For development, use `uv sync --locked`. On headless Ubuntu, install `libosmesa6` and set `MUJOCO_GL=osmesa` and `PYOPENGL_PLATFORM=osmesa` before starting Python.

## Quickstart

```python
import safety_gymnasium2 as sg2

with sg2.make('SafetyPointGoal0-v0') as env:
    observation, info = env.reset(seed=17)
    action = env.action_space.sample()
    observation, reward, cost, terminated, truncated, info = env.step(action)
```

The native `step()` returns six values, including the safety cost. For a five-value Gymnasium API, import the package to register its aliases and read the cost from `info['cost']`.

```python
import gymnasium
import safety_gymnasium2 as sg2

with gymnasium.make('SafetyGymnasium2/SafetyPointGoal0Gymnasium-v0') as env:
    observation, info = env.reset(seed=17)
    observation, reward, terminated, truncated, info = env.step(env.action_space.sample())
    cost = info['cost']
```

See [Basic Usage](https://tran.aerospace.illinois.edu/safety-gymnasium2/introduction/basic_usage.html) for vectorization, rendering, and customization.

## Citing Safety-Gymnasium2

Cite this repository when using the fork in research and record the Git commit used in your experiments.

```bibtex
@misc{safetygymnasium2,
  author = {{Safety Gymnasium 2 Contributors}},
  title = {Safety Gymnasium 2},
  howpublished = {GitHub repository},
  url = {https://github.com/LIRA-illinois/safety-gymnasium2}
}
```

See [CITATION.cff](https://github.com/LIRA-illinois/safety-gymnasium2/blob/main/CITATION.cff) for citation metadata. This fork builds on the [original Safety Gymnasium project](https://github.com/PKU-Alignment/safety-gymnasium) and its [benchmark paper](https://arxiv.org/abs/2310.12567).

## License

The project uses [Apache-2.0](https://github.com/LIRA-illinois/safety-gymnasium2/blob/main/LICENSE). Bundled components have their own notices, including the [MIT license](https://github.com/LIRA-illinois/safety-gymnasium2/blob/main/LICENSE-MIT). See [NOTICE](https://github.com/LIRA-illinois/safety-gymnasium2/blob/main/NOTICE) for provenance.
