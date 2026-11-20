.. Modified for Safety Gymnasium 2.

Safe Multi-Agent
================

MultiGoal extends safe navigation to teams of Point or Ant agents. The
multi-agent velocity tasks use the MaMuJoCo interface, with safety thresholds
for eight configurations across Ant, HalfCheetah, Hopper, Humanoid, Swimmer,
and Walker2d.

.. grid:: 1 2 2 2

   .. grid-item-card:: MultiGoal
      :link: safe_multi_agent/multi_goal
      :link-type: doc

      .. image:: /images/extra_tasks/ant_multigoal1.jpg
         :alt: Two Ant agents in a MultiGoal navigation course

   .. grid-item-card:: Multi-Agent Velocity
      :link: safe_multi_agent/velocity
      :link-type: doc

      .. image:: /images/velocity/ant-2x4-velocity.jpg
         :alt: Ant robot with actuators split between two agents

.. toctree::
   :maxdepth: 1

   safe_multi_agent/multi_goal
   safe_multi_agent/velocity
