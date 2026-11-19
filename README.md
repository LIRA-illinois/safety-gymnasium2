<div align="center">
<h1>
  Safety Gymnasium 2
</h1>
</div>

<div align="center">

  <a>![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-brightgreen.svg)</a>
  <a href="https://safety-gymnasium.readthedocs.io">![Documentation Status](https://img.shields.io/readthedocs/safety-gymnasium?logo=readthedocs)</a>
  <a href="https://github.com/PKU-Alignment/safety-gymnasium/stargazers">![GitHub Repo Stars](https://img.shields.io/github/stars/PKU-Alignment/safety-gymnasium?color=brightgreen&logo=github)</a>
  <a href="https://github.com/PKU-Alignment/safety-gymnasium/blob/HEAD/LICENSE">![License](https://img.shields.io/github/license/PKU-Alignment/safety-gymnasium?label=license&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiBmaWxsPSIjZmZmZmZmIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xMi43NSAyLjc1YS43NS43NSAwIDAwLTEuNSAwVjQuNUg5LjI3NmExLjc1IDEuNzUgMCAwMC0uOTg1LjMwM0w2LjU5NiA1Ljk1N0EuMjUuMjUgMCAwMTYuNDU1IDZIMi4zNTNhLjc1Ljc1IDAgMTAwIDEuNUgzLjkzTC41NjMgMTUuMThhLjc2Mi43NjIgMCAwMC4yMS44OGMuMDguMDY0LjE2MS4xMjUuMzA5LjIyMS4xODYuMTIxLjQ1Mi4yNzguNzkyLjQzMy42OC4zMTEgMS42NjIuNjIgMi44NzYuNjJhNi45MTkgNi45MTkgMCAwMDIuODc2LS42MmMuMzQtLjE1NS42MDYtLjMxMi43OTItLjQzMy4xNS0uMDk3LjIzLS4xNTguMzEtLjIyM2EuNzUuNzUgMCAwMC4yMDktLjg3OEw1LjU2OSA3LjVoLjg4NmMuMzUxIDAgLjY5NC0uMTA2Ljk4NC0uMzAzbDEuNjk2LTEuMTU0QS4yNS4yNSAwIDAxOS4yNzUgNmgxLjk3NXYxNC41SDYuNzYzYS43NS43NSAwIDAwMCAxLjVoMTAuNDc0YS43NS43NSAwIDAwMC0xLjVIMTIuNzVWNmgxLjk3NGMuMDUgMCAuMS4wMTUuMTQuMDQzbDEuNjk3IDEuMTU0Yy4yOS4xOTcuNjMzLjMwMy45ODQuMzAzaC44ODZsLTMuMzY4IDcuNjhhLjc1Ljc1IDAgMDAuMjMuODk2Yy4wMTIuMDA5IDAgMCAuMDAyIDBhMy4xNTQgMy4xNTQgMCAwMC4zMS4yMDZjLjE4NS4xMTIuNDUuMjU2Ljc5LjRhNy4zNDMgNy4zNDMgMCAwMDIuODU1LjU2OCA3LjM0MyA3LjM0MyAwIDAwMi44NTYtLjU2OWMuMzM4LS4xNDMuNjA0LS4yODcuNzktLjM5OWEzLjUgMy41IDAgMDAuMzEtLjIwNi43NS43NSAwIDAwLjIzLS44OTZMMjAuMDcgNy41aDEuNTc4YS43NS43NSAwIDAwMC0xLjVoLTQuMTAyYS4yNS4yNSAwIDAxLS4xNC0uMDQzbC0xLjY5Ny0xLjE1NGExLjc1IDEuNzUgMCAwMC0uOTg0LS4zMDNIMTIuNzVWMi43NXpNMi4xOTMgMTUuMTk4YTUuNDE4IDUuNDE4IDAgMDAyLjU1Ny42MzUgNS40MTggNS40MTggMCAwMDIuNTU3LS42MzVMNC43NSA5LjM2OGwtMi41NTcgNS44M3ptMTQuNTEtLjAyNGMuMDgyLjA0LjE3NC4wODMuMjc1LjEyNi41My4yMjMgMS4zMDUuNDUgMi4yNzIuNDVhNS44NDYgNS44NDYgMCAwMDIuNTQ3LS41NzZMMTkuMjUgOS4zNjdsLTIuNTQ3IDUuODA3eiI+PC9wYXRoPjwvc3ZnPgo=)</a>

</div>

<p align="center">
<a href="https://github.com/PKU-Alignment/safety-gymnasium#why-safety-gymnasium">Why Safety-Gymnasium?</a> |
  <a href="https://www.safety-gymnasium.com">Documentation</a> |
  <a href="#installation">Install guide</a> |
  <a href="https://github.com/PKU-Alignment/safety-gymnasium#customize-your-environments">Customization</a> | <a href="https://sites.google.com/view/safety-gymnasium">Video</a>
</p>

Safety Gymnasium 2 is the LIRA research fork of Safety Gymnasium for safe reinforcement learning.
It aims to deliver a good view of benchmarking SafeRL algorithms and a standardized set of environments.
We provide a set of standard APIs which are compatible with information on constraints.
Users can explore new insights via an elegant code framework and well-designed environments.

## Citing Safety-Gymnasium

If you find Safety-Gymnasium useful, please cite it in your publications.

```bibtex
@inproceedings{ji2023safety,
  title={Safety Gymnasium: A Unified Safe Reinforcement Learning Benchmark},
  author={Jiaming Ji and Borong Zhang and Jiayi Zhou and Xuehai Pan and Weidong Huang and Ruiyang Sun and Yiran Geng and Yifan Zhong and Josef Dai and Yaodong Yang},
  booktitle={Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
  year={2023},
  url={https://openreview.net/forum?id=WZmlxIuIGR}
}
```

--------------------------------------------------------------------------------

## Why Safety-Gymnasium?

Here we provide a table for comparison of **Safety-Gymnasium** and existing SafeRL Environments libraries.

|                                                                                   SafeRL<br/>Envs                                                                                   |            Engine             | Vectorized<br/> Environments | New Gym API<sup>**(3)**</sup> |    Vision Input     |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------: | :--------------------------: | :---------------------------: | :-----------------: |
|            [Safety-Gym](https://github.com/openai/safety-gym)<br/>![GitHub last commit](https://img.shields.io/github/last-commit/openai/safety-gym?label=last%20update)            | `mujoco-py`<sup>**(1)**</sup> |              ❌               |               ❌               | minimally supported |
| [safe-control-gym](https://github.com/utiasDSL/safe-control-gym)<br/>![GitHub last commit](https://img.shields.io/github/last-commit/utiasDSL/safe-control-gym?label=last%20update) |           PyBullet            |              ❌               |               ❌               |          ❌          |
|                                                                       Velocity-Constraints<sup>**(2)**</sup>                                                                        |              N/A              |              ❌               |               ❌               |          ❌          | ❌ |
|    [mujoco-circle](https://github.com/ymzhang01/mujoco-circle)<br/>![GitHub last commit](https://img.shields.io/github/last-commit/ymzhang01/mujoco-circle?label=last%20update)     |            PyTorch            |              ❌               |               ❌               |          ❌          | ❌ |
|                                  Safety-Gymnasium<br/>![GitHub last commit](https://img.shields.io/github/last-commit/PKU-Alignment/safety-gymnasium)                                  |       **MuJoCo 4.0.1+**       |              ✅               |               ✅               |          ✅          |

<sup>(1): Maintenance (expect bug fixes and minor updates); the last commit is 19 Nov 2021. Safety-Gym depends on `mujoco-py` 2.0.2.7, which was updated on Oct 12, 2019.</sup><br/>
<sup>(2): There is no official library for speed-related environments, and its associated cost constraints are constructed from info. But the task is widely used in the study of SafeRL, and we encapsulate it in Safety-Gymnasium.</sup><br/>
<sup>(3): In the gym 0.26.0 release update, a new API of interaction was redefined.</sup>

--------------------------------------------------------------------------------

## Environments

We designed a variety of safety-enhanced learning tasks and integrated the contributions from the RL community: `safety-velocity`, `safety-run`, `safety-circle`, `safety-goal`, `safety-button`, etc.
We introduce a unified safety-enhanced learning benchmark environment library called `Safety-Gymnasium.`

Further, to facilitate the progress of community research, we redesigned [Safety-Gym](https://github.com/openai/safety-gym) and removed the dependency on `mujoco-py`.
We built it on top of [MuJoCo](https://github.com/deepmind/mujoco) and fixed some bugs, more specific bug reports can refer to [Safety-Gym's BUG Report](https://github.com/PKU-Alignment/safety-gymnasium/blob/main/safety_gym_bug_report.md).

Here is a list of all the environments we support for now:

<table border="1">
  <thead>
    <tr>
      <th>Category</th>
      <th>Task</th>
      <th>Agent</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="4">Safe Navigation</td>
      <td>Button[012]</td>
      <td rowspan="4">Point, Car, Doggo, Racecar, Ant</td>
      <td rowspan="4">SafetyPointGoal1-v0</td>
    </tr>
    <tr>
      <td>Goal[012]</td>
    </tr>
    <tr>
      <td>Push[012]</td>
    </tr>
    <tr>
      <td>Circle[012]</td>
    </tr>
    <tr>
      <td>Safe Velocity</td>
      <td>Velocity</td>
      <td>HalfCheetah, Hopper, Swimmer, Walker2d, Ant, Humanoid</td>
      <td>SafetyAntVelocity-v1</td>
    </tr>
    <tr>
      <td rowspan="7">Safe Vision</td>
      <td>BuildingButton[012]</td>
      <td rowspan="7">Point, Car, Doggo, Racecar, Ant</td>
      <td rowspan="7">SafetyFormulaOne1-v0</td>
    </tr>
    <tr>
      <td>BuildingGoal[012]</td>
    </tr>
    <tr>
      <td>BuildingPush[012]</td>
    </tr>
    <tr>
      <td>FadingEasy[012]</td>
    </tr>
    <tr>
      <td>FadingHard[012]</td>
    </tr>
    <tr>
      <td>Race[012]</td>
    </tr>
    <tr>
      <td>FormulaOne[012]</td>
    </tr>
    <tr>
      <td rowspan="8">Safe Multi-Agent</td>
      <td>MultiGoal[012]</td>
      <td>Multi-Point, Multi-Ant</td>
      <td>SafetyAntMultiGoal1-v0</td>
    </tr>
    <tr>
      <td>Multi-Agent Velocity</td>
      <td>6x1HalfCheetah, 2x3HalfCheetah, 3x1Hopper, 2x1Swimmer, 2x3Walker2d, 2x4Ant, 4x2Ant, 9|8Humanoid</td>
      <td>Safety2x4AntVelocity-v0</td>
    </tr>
    <tr>
      <td>FreightFrankaCloseDrawer(Multi-Agent)</td>
      <td rowspan="2">FreightFranka</td>
      <td rowspan="2">FreightFrankaCloseDrawer(Multi-Agent)</td>
    </tr>
    <tr>
      <td>FreightFrankaPickAndPlace(Multi-Agent)</td>
    </tr>
    <tr>
      <td>ShadowHandCatchOver2UnderarmSafeFinger(Multi-Agent)</td>
      <td rowspan="4">ShadowHands</td>
      <td rowspan="4">ShadowHandCatchOver2UnderarmSafeJoint(Multi-Agent)</td>
    </tr>
    <tr>
      <td>ShadowHandCatchOver2UnderarmSafeJoint(Multi-Agent)</td>
    </tr>
    <tr>
      <td>ShadowHandOverSafeFinger(Multi-Agent)</td>
    </tr>
    <tr>
      <td>ShadowHandOverSafeJoint(Multi-Agent)</td>
    </tr>
    <tr>
      <td rowspan="6">Legacy Isaac Gym</td>
      <td>FreightFrankaCloseDrawer</td>
      <td rowspan="2">FreightFranka</td>
      <td rowspan="2">FreightFrankaCloseDrawer</td>
    </tr>
    <tr>
      <td>FreightFrankaPickAndPlace</td>
    </tr>
    <tr>
      <td>ShadowHandCatchOver2UnderarmSafeFinger</td>
      <td rowspan="4">ShadowHands</td>
      <td rowspan="4">ShadowHandCatchOver2UnderarmSafeJoint</td>
    </tr>
    <tr>
      <td>ShadowHandCatchOver2UnderarmSafeJoint</td>
    </tr>
    <tr>
      <td>ShadowHandOverSafeFinger</td>
    </tr>
    <tr>
      <td>ShadowHandOverSafeJoint</td>
    </tr>
  </tbody>
</table>

Here are some screenshots of the **Safe Navigation** tasks.

#### Agents

<table class="docutils align-default">
  <tbody>
    <tr class="row-odd">
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/point_front.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/point_front.jpeg"
              style="width: 130px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="doc">Point</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference" href="agents/car.html"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/car_front.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/car_front.jpeg"
              style="width: 130px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="doc">Car</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference" href="agents/racecar.html"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/racecar_front.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/racecar_front.jpeg"
              style="width: 130px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="doc">Racecar</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference" href="agents/doggo.html"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/doggo_front.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/doggo_front.jpeg"
              style="width: 130px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="doc">Doggo</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference" href="agents/ant.html"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/ant_front.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/ant_front.jpeg"
              style="width: 130px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="doc">Ant</span></a></strong>
        </p>
      </td>
    </tr>
  </tbody>
</table>

#### Tasks

<table class="docutils align-default">
  <tbody>
    <tr class="row-odd">
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/goal0.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/goal0.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Goal0</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/goal1.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/goal1.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Goal1</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/goal2.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/goal2.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Goal2</span></a></strong>
        </p>
      </td>
    </tr>
    <tr class="row-even">
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/button0.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/button0.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Button0</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference" href="./button#button1"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/button1.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/button1.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Button1</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference" href="./button#button2"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/button2.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/button2.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Button2</span></a></strong>
        </p>
      </td>
    </tr>
    <tr class="row-odd">
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/push0.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/push0.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Push0</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/push1.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/push1.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Push1</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/push2.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/push2.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Push2</span></a></strong>
        </p>
      </td>
    </tr>
    <tr class="row-even">
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/circle0.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/circle0.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Circle0</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/circle1.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/circle1.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Circle1</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference" href="./circle#circle2"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/circle2.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/images/circle2.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Circle2</span></a></strong>
        </p>
      </td>
    </tr>
  </tbody>
</table>

### Vision-based Safe RL

Vision-based SafeRL lacks realistic scenarios.
Although the original `Safety-Gym` could minimally support visual input, the scenarios were too similar.
To facilitate the validation of visual-based SafeRL algorithms, we have developed a set of realistic vision-based SafeRL tasks, which are currently being validated on the baseline.

For the appetizer, the images are as follows:

<table class="docutils align-default">
  <tbody>
    <tr class="row-odd">
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/race0.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/race0.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Race0</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/race1.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/race1.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Race1</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/race2.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/race2.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">Race2</span></a></strong>
        </p>
      </td>
    </tr>
    <tr class="row-odd">
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/formula_one0.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/formula_one0.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">FormulaOne0</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/formula_one1.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/formula_one1.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">FormulaOne1</span></a></strong>
        </p>
      </td>
      <td>
        <figure class="align-default">
          <a class="reference external image-reference"><img
              alt="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/formula_one2.jpeg"
              src="https://github.com/PKU-Alignment/safety-gymnasium/raw/HEAD/docs/_static/images/formula_one2.jpeg" style="width: 230px;"></a>
        </figure>
        <p class="centered">
          <strong><a class="reference internal"><span class="std std-ref">FormulaOne2</span></a></strong>
        </p>
      </td>
    </tr>
  </tbody>
</table>

### Environment Usage

**Notes:** We support explicitly expressing the `cost` based on [**Gymnasium APIs**](https://github.com/Farama-Foundation/Gymnasium).
The `step` method returns 6 items `(next_obervation, reward, cost, terminated, truncated, info)` with an extra `cost` field.

```python
import safety_gymnasium2

env_id = 'SafetyPointGoal1-v0'
env = safety_gymnasium2.make(env_id)

obs, info = env.reset()
while True:
    act = env.action_space.sample()
    obs, reward, cost, terminated, truncated, info = env.step(act)
    if terminated or truncated:
        break
    env.render()
```

We also provide two convenience wrappers for converting the Safety-Gymnasium environment to the standard Gymnasium API and vice versa.

```python
# Safety-Gymnasium API: step returns (next_obervation, reward, cost, terminated, truncated, info)
# Gymnasium API:        step returns (next_obervation, reward, terminated, truncated, info) and cost is in the `info` dict associated with a str key `'cost'`

safety_gymnasium2_env = safety_gymnasium2.make(env_id)
gymnasium_env = safety_gymnasium2.wrappers.SafetyGymnasium2Gymnasium(safety_gymnasium2_env)

safety_gymnasium2_env = safety_gymnasium2.wrappers.Gymnasium2SafetyGymnasium(gymnasium_env)
```

Users can apply Gymnasium wrappers easily with:

```python
import gymnasium
import safety_gymnasium2

def make_safe_env(env_id):
    safe_env = safety_gymnasium2.make(env_id)
    env = safety_gymnasium2.wrappers.SafetyGymnasium2Gymnasium(safe_env)
    env = gymnasium.wrappers.SomeWrapper1(env)
    env = gymnasium.wrappers.SomeWrapper2(env, argname1=arg1, argname2=arg2)
    ...
    env = gymnasium.wrappers.SomeWrapperN(env)
    safe_env = safety_gymnasium2.wrappers.Gymnasium2SafetyGymnasium(env)
    return safe_env
```

or

```python
import functools

import gymnasium
import safety_gymnasium2

def make_safe_env(env_id):
    return safety_gymnasium2.wrappers.with_gymnasium_wrappers(
        safety_gymnasium2.make(env_id),
        gymnasium.wrappers.SomeWrapper1,
        functools.partial(gymnasium.wrappers.SomeWrapper2, argname1=arg1, argname2=arg2),
        ...,
        gymnasium.wrappers.SomeWrapperN,
    )
```

Single-agent tasks also have standard Gymnasium IDs under `SafetyGymnasium2/`. Their five-value `step()` puts the safety cost in `info["cost"]`.

```python
import gymnasium
import safety_gymnasium2 as sg2

safe_env = sg2.make('SafetyPointGoal1-v0')
gym_env = gymnasium.make('SafetyGymnasium2/SafetyPointGoal1Gymnasium-v0')
```

--------------------------------------------------------------------------------

## Installation

The core package requires Python 3.11 or newer. From a checkout, install it in an active virtual environment with `python -m pip install .`, or use `uv sync --locked` for development.

Race and FormulaOne use the `racing` extra. Building uses the `building` extra. Install either or both from the checkout with `uv`:

```bash
uv sync --locked --extra racing --extra building
```

To use `pip` with the optional asset wheels, build the local workspace first:

```bash
uv build --all-packages --no-sources
python -m pip install --find-links ./dist 'safety-gymnasium2[racing,building]'
```

On headless Ubuntu, install `libosmesa6` and set `MUJOCO_GL=osmesa` before starting Python. Isaac Gym and Safe VLA use separate legacy setups. See [legacy integrations](legacy/README.md).

### Benchmark versions

`Safety{Robot}Velocity-v0` and `-v1` use Gymnasium's v4 locomotion implementations. `-v2` uses upstream v5 observations, rewards, and termination with Safety Velocity v1 costs and horizons. Ant observations change from 27 to 105 values by default, and Humanoid observations change from 376 to 348. The Robotics upgrade also changes some multi-agent observation shapes. For example, Ant with `2x4` changes from 21 to 63 values per agent. Record the task ID, fork revision, resolved dependencies, and seed with each experiment.

## Debug with your keyboard

For simple agents, we offer the capability to control the robot's movement via the keyboard, facilitating debugging. Simply append a **Debug** suffix to the task name, such as `SafetyCarGoal2Debug-v0`, and utilize the keys `I`, `K`, `J`, and `L` to guide the robot's movement.

For more intricate agents, you can also craft custom control logic based on specific peripherals. To achieve this, implement the `debug` method from the `BaseAgent` for the designated agent.



## Customize your environments

We construct a highly expandable framework of code so that you can easily comprehend it and design your environments to facilitate your research with no more than 100 lines of code on average.

For details, please refer to our [documentation](https://www.safety-gymnasium.com/en/latest/components_of_environments/tasks/task_example.html).
Here is a minimal example:

```python
# import the objects you want to use
# or you can define specific objects by yourself, just make sure obeying our specification
from safety_gymnasium2.assets.geoms import Apples
from safety_gymnasium2.bases import BaseTask

# inherit the basetask
class MytaskLevel0(BaseTask):
    def __init__(self, config):
        super().__init__(config=config)
        # define some properties
        self.num_steps = 500
        self.agent.placements = [(-0.8, -0.8, 0.8, 0.8)]
        self.agent.keepout = 0
        self.lidar_conf.max_dist = 6
        # add objects into environments
        self.add_geoms(Apples(num=2, size=0.3))

    def calculate_reward(self):
        # implement your reward function
        # Note: cost calculation is based on objects, so it's automatic
        reward = 1
        return reward

    def specific_reset(self):
        # depending on your task

    def specific_step(self):
        # depending on your task

    def update_world(self):
        # depending on your task

    @property
    def goal_achieved(self):
        # depending on your task
```


## License

Safety-Gymnasium is released under Apache License 2.0.
