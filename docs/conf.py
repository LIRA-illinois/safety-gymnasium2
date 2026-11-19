"""Configuration for the Sphinx documentation build."""

from importlib.metadata import version as package_version
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.util.tags import Tags

    tags: Tags


project = 'Safety Gymnasium 2'
copyright = '2023, PKU-Alignment'
author = 'PKU-Alignment'
release = package_version('safety-gymnasium2')
version = release

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx_design',
]
# Sphinx injects the active build tags into this configuration.
if tags.has('spelling'):  # noqa: F821
    extensions.append('sphinxcontrib.spelling')

templates_path = ['_templates']
exclude_patterns = []


napoleon_use_ivar = True
napoleon_use_admonition_for_references = True
# See https://github.com/sphinx-doc/sphinx/issues/9119
napoleon_custom_sections = [('Returns', 'params_style')]

autoclass_content = 'both'
autodoc_preserve_defaults = True

html_theme = 'furo'
html_title = 'Safety-Gymnasium Documentation'
html_baseurl = 'https://www.safety-gymnasium.com'
html_copy_source = False
html_context: dict[str, str | bool] = {
    'conf_py_path': '/docs/',
    'display_github': False,
    'github_user': 'PKU-Alignment',
    'github_repo': 'safety-gymnasium',
    'github_version': 'main',
    'slug': 'safety-gymnasium',
}

html_static_path = ['_static']
html_css_files = []
