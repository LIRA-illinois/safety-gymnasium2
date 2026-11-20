"""Bundled HalfCheetah model and its legacy mass normalization."""

from __future__ import annotations

from pathlib import Path

import mujoco
from gymnasium.envs.mujoco import mujoco_env

DEFAULT_HALF_CHEETAH_XML = 'half_cheetah.xml'
HALF_CHEETAH_XML_PATH = str(
    Path(__file__).resolve().parents[2] / 'assets' / 'xmls' / DEFAULT_HALF_CHEETAH_XML
)
_UPSTREAM_HALF_CHEETAH_XML = (
    Path(mujoco_env.__file__).with_name('assets') / DEFAULT_HALF_CHEETAH_XML
)


class BundledHalfCheetahModel(mujoco_env.MujocoEnv):
    """Simulation initializer for the default single-agent HalfCheetah model."""

    def _initialize_simulation(self) -> tuple[mujoco.MjModel, mujoco.MjData]:  # ty: ignore[missing-attribute]
        if Path(self.fullpath) != _UPSTREAM_HALF_CHEETAH_XML:
            return super()._initialize_simulation()

        self.fullpath = HALF_CHEETAH_XML_PATH
        model, data = super()._initialize_simulation()
        scale_half_cheetah_model(model, data)
        return model, data


def scale_half_cheetah_model(model: mujoco.MjModel, data: mujoco.MjData) -> None:  # ty: ignore[missing-attribute]
    """Apply the legacy mass scaling to the bundled model before the first reset."""
    mujoco.mj_setTotalmass(model, 14.0)  # ty: ignore[missing-attribute]
    mujoco.mj_setConst(model, data)  # ty: ignore[missing-attribute]
    # The viewer uses mean mass to scale perturbations, excluding the world body.
    model.stat.meanmass = float(model.body_mass[1:].mean())
