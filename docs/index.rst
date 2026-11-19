
Safety Gymnasium 2
==================

Safety Gymnasium 2 provides MuJoCo environments for safe reinforcement learning.

.. image:: _static/images/car_demo.gif
   :alt: racecar
   :width: 500
   :align: center

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
   environments/safe_vision
   environments/safe_multi_agent
   environments/safe_isaac_gym


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
