.. Modified for Safety Gymnasium 2.

Safe Navigation
===============

The catalog includes Goal, Button, Push, Circle, Run, FadingEasy, and FadingHard. The Fading tasks in this release use state observations.

Navigation tasks are an important class of tasks that apply RL to reality, requiring an agent to continuously change its position and interact with objects in the environment in order to accomplish a specified goal, which is usually associated with a specific position or movement pattern. In Safe RL, the focus is on the behavioral paradigm of whether an intelligent body, as a free-moving individual, can accomplish tasks in the environment without dangerous collisions or contact.

We have refactored and optimized the widely used but unmaintained and lacking supports environment library `Safety-Gym <https://github.com/openai/safety-gym>`__ in the library, and we have also carefully designed new environments and agents to take into account changing requirements, increasing computational power and advances in algorithms, which will be gradually Released in the coming period.


Goal, Button, Push, and Circle
------------------------------

.. grid:: 1 2 3 3

   .. grid-item-card:: Goal level 0
      :link: Goal0
      :link-type: ref

      .. image:: ../../images/readme/goal0.jpg
         :alt: Point in Goal level 0

   .. grid-item-card:: Goal level 1
      :link: Goal1
      :link-type: ref

      .. image:: ../../images/readme/goal1.jpg
         :alt: Point in Goal level 1

   .. grid-item-card:: Goal level 2
      :link: Goal2
      :link-type: ref

      .. image:: ../../images/readme/goal2.jpg
         :alt: Point in Goal level 2

   .. grid-item-card:: Button level 0
      :link: Button0
      :link-type: ref

      .. image:: ../../images/readme/button0.jpg
         :alt: Point in Button level 0

   .. grid-item-card:: Button level 1
      :link: Button1
      :link-type: ref

      .. image:: ../../images/readme/button1.jpg
         :alt: Point in Button level 1

   .. grid-item-card:: Button level 2
      :link: Button2
      :link-type: ref

      .. image:: ../../images/readme/button2.jpg
         :alt: Point in Button level 2

   .. grid-item-card:: Push level 0
      :link: Push0
      :link-type: ref

      .. image:: ../../images/readme/push0.jpg
         :alt: Point in Push level 0

   .. grid-item-card:: Push level 1
      :link: Push1
      :link-type: ref

      .. image:: ../../images/readme/push1.jpg
         :alt: Point in Push level 1

   .. grid-item-card:: Push level 2
      :link: Push2
      :link-type: ref

      .. image:: ../../images/readme/push2.jpg
         :alt: Point in Push level 2

   .. grid-item-card:: Circle level 0
      :link: Circle0
      :link-type: ref

      .. image:: ../../images/readme/circle0.jpg
         :alt: Point in Circle level 0

   .. grid-item-card:: Circle level 1
      :link: Circle1
      :link-type: ref

      .. image:: ../../images/readme/circle1.jpg
         :alt: Point in Circle level 1

   .. grid-item-card:: Circle level 2
      :link: Circle2
      :link-type: ref

      .. image:: ../../images/readme/circle2.jpg
         :alt: Point in Circle level 2


Run
---

.. figure:: /images/extra_tasks/point_run0.jpg
   :alt: The Point robot between the boundary walls of the Run track.
   :width: 540px
   :align: center

   ``SafetyPointRun0-v0``

Fading
------

The screenshots show each task after 60 steps from the same reset seed. Objects
fade faster in FadingHard.

.. list-table::
   :header-rows: 1

   * - Task
     - Level 0
     - Level 1
     - Level 2
   * - FadingEasy
     - .. image:: /images/extra_tasks/point_fading_easy0.jpg
          :alt: Point and its partially faded goal in FadingEasy level 0.
     - .. image:: /images/extra_tasks/point_fading_easy1.jpg
          :alt: Point, its goal, and hazards after 60 steps in FadingEasy level 1.
     - .. image:: /images/extra_tasks/point_fading_easy2.jpg
          :alt: Point, its goal, hazards, and vases after 60 steps in FadingEasy level 2.
   * - FadingHard
     - .. image:: /images/extra_tasks/point_fading_hard0.jpg
          :alt: Point and its nearly transparent goal in FadingHard level 0.
     - .. image:: /images/extra_tasks/point_fading_hard1.jpg
          :alt: Point, its goal, and hazards after 60 steps in FadingHard level 1.
     - .. image:: /images/extra_tasks/point_fading_hard2.jpg
          :alt: Point, its goal, hazards, and vases after 60 steps in FadingHard level 2.


.. toctree::
    :hidden:

    safe_navigation/circle.rst
    safe_navigation/goal.rst
    safe_navigation/button.rst
    safe_navigation/push.rst
