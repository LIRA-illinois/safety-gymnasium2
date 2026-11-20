<!-- Modified for Safety Gymnasium 2. -->
# Safety Gymnasium benchmark history

The original Safety Gymnasium project collected its historical results with [OmniSafe](https://github.com/PKU-Alignment/omnisafe). The upstream report lists an AMD EPYC 7H12 processor, the OmniSafe default algorithm settings, and seeds 0, 5, 10, 15, and 20. The plots describe the upstream software stack. See the [original benchmark figures](https://github.com/PKU-Alignment/safety-gymnasium/tree/ae966e511b9927f06b39c727ca5c650136a4e696/benchmarks).

## Reproducing new runs

Record the following next to the results of each Safety Gymnasium 2 run.

- The fork commit (`git rev-parse HEAD`) and any local changes (`git status --short`).
- The environment ID, constructor configuration, episode horizon, wrapper order and settings, and environment and learner seeds.
- The Python version, platform, renderer and hardware if relevant, `uv.lock`, the installed package versions (`uv pip freeze`), and the versions of any installed asset packs.
- The learner and configuration used, including its repository commit if it is developed separately. The [built-in OmniSafe adapter](https://github.com/PKU-Alignment/omnisafe/blob/main/omnisafe/envs/safety_gymnasium_env.py) imports the original `safety_gymnasium` package. Verify the trainer loads `safety_gymnasium2` for fork experiments.

Run the same-stack fixed-action replay check with `uv run --locked --group test python -m unittest discover -s tests -p 'test_research_contracts.py' -k replay`. It checks repeatability within the installed simulation stack. Record dependency changes when comparing results across stacks.
