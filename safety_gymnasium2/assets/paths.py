# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
# ==============================================================================
"""Locate optional meshes and textures installed by the task extras."""

from __future__ import annotations

import functools
import pathlib
from collections.abc import Iterable, MutableMapping
from importlib import util

_ASSET_PACKAGES = {
    'racing': ('racing', 'safety_gymnasium2_racing_assets'),
    'building-structure': ('building', 'safety_gymnasium2_building_structure'),
    'building-scenery': ('building', 'safety_gymnasium2_building_scenery'),
}


@functools.cache
def _asset_package_path(asset_pack: str) -> pathlib.Path:
    extra, package = _ASSET_PACKAGES[asset_pack]
    spec = util.find_spec(package)
    if spec is None or spec.origin is None:
        raise ImportError(
            f'{extra.capitalize()} tasks require optional assets. '
            f'From the checkout, run uv sync --extra {extra}. '
            f'From local builds in dist, run pip install --find-links dist "safety-gymnasium2[{extra}]".',
        )
    return pathlib.Path(spec.origin).parent


def require_task_assets(task_name: str) -> None:
    """Raise an installation hint if a task's optional assets are unavailable."""
    if task_name.startswith(('RaceLevel', 'FormulaOneLevel')):
        _asset_package_path('racing')
    elif task_name.startswith('Building'):
        _asset_package_path('building-structure')
        _asset_package_path('building-scenery')


def resolve_asset_files(assets: Iterable[MutableMapping[str, str]], directory: str) -> None:
    """Replace optional asset references in generated MJCF with local paths."""
    for asset in assets:
        for attribute, filename in asset.items():
            if not attribute.startswith('@file'):
                continue
            asset_pack, separator, basename = filename.partition('/')
            if separator and asset_pack in _ASSET_PACKAGES:
                asset[attribute] = str(_asset_package_path(asset_pack) / directory / basename)
