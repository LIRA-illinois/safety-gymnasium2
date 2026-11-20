.. Modified for Safety Gymnasium 2.

Basic Usage
===========

Installation
------------

Safety Gymnasium 2 requires Python 3.11 or newer. Install from a checkout using
``python -m pip install .`` in an active virtual environment, or use
``uv sync --locked`` for development.


Specification
-------------

The native Safety Gymnasium 2 API returns observation, reward, cost,
termination, truncation, and info from ``step()``. Single-agent Gymnasium
aliases under ``SafetyGymnasium2/`` return five values and carry the safety
cost in ``info["cost"]``. See the `Gymnasium API documentation
<https://gymnasium.farama.org/api/env/>`__ for the standard interface.

Initializing the environment
----------------------------

Run the headless examples with ``uv run --locked python examples/quickstart.py``.

.. code-block:: python

    from contextlib import closing

    import safety_gymnasium2 as sg2

.. literalinclude:: ../../examples/quickstart.py
   :language: python
   :pyobject: single_environment

For a Gymnasium alias, import ``safety_gymnasium2`` to register the IDs and
then use ``gymnasium.make('SafetyGymnasium2/SafetyPointGoal0Gymnasium-v0',
max_episode_steps=2)``. Use ``max_episode_steps`` to set the alias horizon.
The alias and its ``unwrapped`` environment both return the five-value
Gymnasium step. Use ``env.unwrapped.native_env`` to access the native
environment directly.

Vector environments
-------------------

.. literalinclude:: ../../examples/quickstart.py
   :language: python
   :pyobject: vector_environments

On a finished lane, ``next_obs`` contains the reset observation. The mask
``info['_final_observation']`` marks lanes with a saved terminal observation
in ``info['final_observation']``. Preserve those terminal observations in
replay buffers and use the returned reset observations to choose the next
actions. For workers started with ``spawn``, pass
``multiprocessing_context='spawn'`` to ``sg2.vector.make()`` and construct the
vector environment under the script's ``if __name__ == '__main__':`` guard.

Observation Space
-----------------

.. code-block:: python

    env = safety_gymnasium2.make('SafetyPointCircle0-v0', render_mode='human')
    obs, info = env.reset()
    print(env.observation_space)
    '''
    Box([-inf -inf -inf -inf -inf -inf -inf -inf -inf -inf -inf -inf   0.   0.
    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.],
    [inf inf inf inf inf inf inf inf inf inf inf inf  1.  1.  1.  1.  1.  1.
    1.  1.  1.  1.  1.  1.  1.  1.  1.  1.], (28,), float64)
    '''


    print(env.get_wrapper_attr('obs_space_dict'))
    '''
    Dict('accelerometer': Box(-inf, inf, (3,), float64),
         'velocimeter': Box(-inf, inf, (3,), float64),
         'gyro': Box(-inf, inf, (3,), float64),
         'magnetometer': Box(-inf, inf, (3,), float64),
         'circle_lidar': Box(0.0, 1.0, (16,), float64))
    '''


    # position of each part in the obs is as same as it appears in the Dict above.
    print(obs)
    '''
	[0.         0.         9.81       0.         0.         0.
    0.         0.         0.         0.36647163 0.34014489 0.
    0.         0.         0.         0.         0.         0.
    0.         0.         0.         0.         0.         0.08518475
    0.93364224 0.84845749 0.         0.        ]
    '''


Action Space
------------

.. code-block:: python

    env = safety_gymnasium2.make('SafetyPointCircle0-v0', render_mode='human')
    obs, info = env.reset()
    print(env.action_space)
    # Box(-1.0, 1.0, (2,), float64)

Render
------

We completely inherit the excellent API for render in Gymnasium.

.. Note::

    The set of supported modes varies per environment. (And some
    third-party environments may not support rendering at all.)
    By convention, if render_mode is:

    - **None (default)**: no render is computed.
    - **human**: render return None.
      The environment is continuously rendered in the current display or terminal. Usually for human consumption.
    - **rgb_array**: return a single frame representing the current state of the environment.
      A frame is a numpy.ndarray with shape (x, y, 3) representing RGB values for an x-by-y pixel image.
    - **rgb_array_list**: return a list of frames representing the states of the environment since the last reset.
      Each frame is a numpy.ndarray with shape (x, y, 3), as with `rgb_array`.
    - **depth_array**: return a single frame representing the current state of the environment.
      A frame is a numpy.ndarray with shape (x, y) representing depth values for an x-by-y pixel image.
    - **depth_array_list**: return a list of frames representing the states of the environment since the last reset.
      Each frame is a numpy.ndarray with shape (x, y), as with `depth_array`.

Debug with your keyboard
------------------------

.. Note::

    For simple agents, we offer the capability to control the robot's movement via the keyboard, facilitating debugging. Simply append a **Debug** suffix to the task name, such as **SafetyCarGoal2Debug-v0**, and utilize the keys `I`, `K`, `J`, and `L` to guide the robot's movement.

    For more intricate agents, you can also craft custom control logic based on specific peripherals. To achieve this, implement the `debug` method from the `BaseAgent` for the designated agent.
