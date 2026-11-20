.. Modified for Safety Gymnasium 2.

Safe Navigation
===============

The catalog includes Goal, Button, Push, Circle, Run, FadingEasy, and FadingHard. The Fading tasks in this release use state observations.

Navigation tasks are an important class of tasks that apply RL to reality, requiring an agent to continuously change its position and interact with objects in the environment in order to accomplish a specified goal, which is usually associated with a specific position or movement pattern. In Safe RL, the focus is on the behavioral paradigm of whether an intelligent body, as a free-moving individual, can accomplish tasks in the environment without dangerous collisions or contact.

We have refactored and optimized the widely used but unmaintained and lacking supports environment library `Safety-Gym <https://github.com/openai/safety-gym>`__ in the library, and we have also carefully designed new environments and agents to take into account changing requirements, increasing computational power and advances in algorithms, which will be gradually Released in the coming period.


.. toctree::
    :hidden:

    safe_navigation/circle.rst
    safe_navigation/goal.rst
    safe_navigation/button.rst
    safe_navigation/push.rst
