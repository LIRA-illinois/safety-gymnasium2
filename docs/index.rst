.. Modified for Safety Gymnasium 2.


Safety Gymnasium 2
==================

Safety Gymnasium 2 provides MuJoCo environments for safe reinforcement learning.


.. figure:: /images/navigation-hero.jpg
   :alt: Racecar, a green goal, and blue hazards on a MuJoCo navigation course
   :width: 720px
   :align: center

   Racecar in Goal level 1.


The headless quickstart demonstrates the single and vector APIs. Vector lanes
reset on the step when their episodes finish. Use the terminal observation
mask to recover the pre-reset observations for replay.

.. literalinclude:: ../examples/quickstart.py
   :language: python

.. toctree::
   :hidden:
   :caption: INTRODUCTION

   introduction/about_safety_gymnasium
   introduction/basic_usage


.. toctree::
   :hidden:
   :caption: COMPONENTS OF ENVIRONMENTS

   components_of_environments/agents
   components_of_environments/objects
   components_of_environments/tasks


.. toctree::
   :hidden:
   :caption: ENVIRONMENTS

   environments/safe_navigation
   environments/safe_velocity
   environments/safe_multi_agent


.. toctree::
   :hidden:
   :caption: API

   api/bases
   api/builder
   api/utils


.. toctree::
   :hidden:
   :caption: Development

`GitHub <https://github.com/LIRA-illinois/safety-gymnasium2>`__

`Contribute to the Docs <https://github.com/LIRA-illinois/safety-gymnasium2/blob/main/CONTRIBUTING.md>`__
