# Legacy integrations

Isaac Gym and Safe VLA live here in their historical Python namespace. Use a
separate virtual environment for each integration. Add this `legacy` directory
to `PYTHONPATH` in that environment to resolve the original
`safety_gymnasium.tasks.safe_isaac_gym` or `safety_gymnasium.tasks.safe_vla`
imports from a checkout.

Isaac Gym requires its NVIDIA SDK and the CUDA and PyTorch versions expected by
that SDK. Safe VLA uses the original SPOC project environment, including its
AllenAct and AI2-THOR dependencies and project modules. Consult the upstream
integration setup for the required SDK or project revision.
