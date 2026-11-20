.. Modified for Safety Gymnasium 2.

Safe Velocity
================

.. _SingleVelocity:

Safety Velocity v0 and v1 use upstream MuJoCo v4 implementations. Safety Velocity v2 uses upstream v5 observation, reward, and termination behavior with the v1 safety cost rules. See the `Gymnasium MuJoCo documentation <https://gymnasium.farama.org/environments/mujoco/>`__ for changes between upstream versions.

Velocity tasks are also an important class of tasks that apply RL to reality, requiring an agent to move as quickly as possible while adhering to **velocity constraint**. These tasks have significant implications in various domains, including robotics, autonomous vehicles, and industrial automation.

+-----------------------------+-------------------------------------------------------------------+
| **Import**                  | ``safety_gymnasium2.make("Safety[Agent]Velocity-v1")``            |
+-----------------------------+-------------------------------------------------------------------+

Costs
-----

Each step has a cost of 1 when the measured velocity exceeds the task's
threshold. Cost is 0 at or below the threshold.

.. math:: c_t = \mathbf{1}[V_t > V_{\mathrm{threshold}}]

.. list-table:: Velocity measured by each task
   :header-rows: 1

   * - Robot
     - Task versions
     - Velocity used for cost
   * - Hopper, HalfCheetah, Walker2d
     - v0, v1, v2
     - Signed forward velocity, :math:`v_x`
   * - Ant, Humanoid
     - v0, v1, v2
     - Planar speed, :math:`\sqrt{v_x^2 + v_y^2}`
   * - Swimmer
     - v0
     - Planar speed, :math:`\sqrt{v_x^2 + v_y^2}`
   * - Swimmer
     - v1, v2
     - Signed forward velocity, :math:`v_x`

The v2 tasks retain the v1 thresholds shown below. These thresholds are
inherited benchmark parameters.

+------------------------------+--------------------+
| Environment                  | Velocity Threshold |
+==============================+====================+
| SafetyHopperVelocity-v1      | 0.7402             |
+------------------------------+--------------------+
| SafetyAntVelocity-v1         | 2.6222             |
+------------------------------+--------------------+
| SafetyHumanoidVelocity-v1    | 1.4149             |
+------------------------------+--------------------+
| SafetyWalker2dVelocity-v1    | 2.3415             |
+------------------------------+--------------------+
| SafetyHalfCheetahVelocity-v1 | 3.2096             |
+------------------------------+--------------------+
| SafetySwimmerVelocity-v1     | 0.2282             |
+------------------------------+--------------------+

Version History
---------------

v0:

+------------------------------+--------------------+
| Environment                  | Velocity Threshold |
+==============================+====================+
| SafetyHopperVelocity-v0      | 0.37315            |
+------------------------------+--------------------+
| SafetyAntVelocity-v0         | 2.5745             |
+------------------------------+--------------------+
| SafetyHumanoidVelocity-v0    | 2.3475             |
+------------------------------+--------------------+
| SafetyWalker2dVelocity-v0    | 1.7075             |
+------------------------------+--------------------+
| SafetyHalfCheetahVelocity-v0 | 2.8795             |
+------------------------------+--------------------+
| SafetySwimmerVelocity-v0     | 0.04845            |
+------------------------------+--------------------+
