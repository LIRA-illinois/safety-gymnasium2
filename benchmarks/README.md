# Safety Gymnasium benchmark history

The figures below are inherited results from the original Safety Gymnasium project, collected with [OmniSafe](https://github.com/PKU-Alignment/omnisafe). The upstream report lists an AMD EPYC 7H12 processor, the OmniSafe default algorithm settings, and seeds 0, 5, 10, 15, and 20. These plots describe the upstream software stack.

## Reproducing new runs

Record the following next to the results of each Safety Gymnasium 2 run.

- The fork commit (`git rev-parse HEAD`) and any local changes (`git status --short`).
- The environment ID, constructor configuration, episode horizon, wrapper order and settings, and environment and learner seeds.
- The Python version, platform, renderer and hardware if relevant, `uv.lock`, the installed package versions (`uv pip freeze`), and the versions of any installed asset packs.
- The learner and configuration used, including its repository commit if it is developed separately. The [built-in OmniSafe adapter](https://github.com/PKU-Alignment/omnisafe/blob/main/omnisafe/envs/safety_gymnasium_env.py) imports the original `safety_gymnasium` package. Verify the trainer loads `safety_gymnasium2` for fork experiments.

Run the same-stack fixed-action replay check with `uv run --locked --group test python -m unittest discover -s tests -p 'test_research_contracts.py' -k replay`. It checks repeatability within the installed simulation stack. Record dependency changes when comparing results across stacks.

## Upstream benchmark figures

### SafetyAntVelocity-v1(1e6)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_ant_1e6.png">
    <br>
</center>

### SafetyAntVelocity-v1(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_ant_1e7.png">
    <br>
</center>

### SafetyHalfCheetahVelocity-v1(1e6)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_halfcheetah_1e6.png">
    <br>
</center>

### SafetyHalfCheetahVelocity-v1(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_halfcheetah_1e7.png">
    <br>
</center>

### SafetyHopperVelocity-v1(1e6)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_hopper_1e6.png">
    <br>
</center>

### SafetyHopperVelocity-v1(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_hopper_1e7.png">
    <br>
</center>

### SafetyHumanoidVelocity-v1(1e6)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_humanoid_1e6.png">
    <br>
</center>

### SafetyHumanoidVelocity-v1(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_humanoid_1e7.png">
    <br>
</center>

### SafetyWalker2dVelocity-v1(1e6)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_walker2d_1e6.png">
    <br>
</center>

### SafetyWalker2dVelocity-v1(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_walker2d_1e7.png">
    <br>
</center>

### SafetySwimmerVelocity-v1(1e6)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_swimmer_1e6.png">
    <br>
</center>

### SafetySwimmerVelocity-v1(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_swimmer_1e7.png">
    <br>
</center>

### SafetyPointGoal0-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointgoal0_1e7.png">
    <br>
</center>

### SafetyPointGoal1-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointgoal1_1e7.png">
    <br>
</center>

### SafetyPointGoal2-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointgoal2_1e7.png">
    <br>
</center>

### SafetyCarGoal0-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_cargoal0_1e7.png">
    <br>
</center>

### SafetyCarGoal1-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_cargoal1_1e7.png">
    <br>
</center>

### SafetyCarGoal2-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_cargoal2_1e7.png">
    <br>
</center>

### SafetyPointButton0-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointbutton0_1e7.png">
    <br>
</center>

### SafetyPointButton1-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointbutton1_1e7.png">
    <br>
</center>

### SafetyPointButton2-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointbutton2_1e7.png">
    <br>
</center>

### SafetyCarButton0-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_carbutton0_1e7.png">
    <br>
</center>

### SafetyCarButton1-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_carbutton1_1e7.png">
    <br>
</center>

### SafetyCarButton2-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_carbutton2_1e7.png">
    <br>
</center>

### SafetyPointPush0-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointpush0_1e7.png">
    <br>
</center>

### SafetyPointPush1-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointpush1_1e7.png">
    <br>
</center>

### SafetyPointPush2-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointpush2_1e7.png">
    <br>
</center>

### SafetyCarPush0-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_carpush0_1e7.png">
    <br>
</center>

### SafetyCarPush1-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_carpush1_1e7.png">
    <br>
</center>

### SafetyCarPush2-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_carpush2_1e7.png">
    <br>
</center>

### SafetyPointCircle0-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointcircle0_1e7.png">
    <br>
</center>

### SafetyPointCircle1-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointcircle1_1e7.png">
    <br>
</center>

### SafetyPointCircle2-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_pointcircle2_1e7.png">
    <br>
</center>

### SafetyCarCircle0-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_carcircle0_1e7.png">
    <br>
</center>

### SafetyCarCircle1-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_carcircle1_1e7.png">
    <br>
</center>

### SafetyCarCircle2-v0(1e7)
<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);"
    src="./benchmarks/first_order_carcircle2_1e7.png">
    <br>
</center>
