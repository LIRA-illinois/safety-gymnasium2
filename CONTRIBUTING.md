<!-- Modified for Safety Gymnasium 2. -->
# Contributing to Safety Gymnasium 2

Use the [fork's issue tracker](https://github.com/LIRA-illinois/safety-gymnasium2/issues) to discuss bugs and feature proposals. Open pull requests against `main` and describe the behavior change and how you checked it.

## Development setup

```bash
git clone https://github.com/LIRA-illinois/safety-gymnasium2.git
cd safety-gymnasium2
uv sync --locked --group test --group lint --group docs
```

On headless Ubuntu, install `libosmesa6` and set `MUJOCO_GL=osmesa` and `PYOPENGL_PLATFORM=osmesa` before running rendering tests.

## Tests and checks

Tests use `absl.testing`. Add regression coverage for behavior changes and close environments with `addCleanup` or a context manager.

```bash
make test
make test TESTOPTS='-k episode_limit'
make commit-checks
make docs-build
```

`make test` writes the XML coverage report to `tests/coverage.xml`. `make commit-checks` runs Ruff lint and format checks and the scoped `ty` check used by CI. Import ordering and formatting checks cover the compatibility layer, tests, examples, and docs. Use `make format` on that scope or pass `FORMAT_PATHS` to select other files. `make type` runs the full-package type check.

Optional Git hooks run the same Python checks and inspect repository files. Install them with `uv run --locked --group lint pre-commit install` and run them on the whole checkout with `make pre-commit`.

Document user-visible changes in `CHANGELOG.md`. Use the upstream benchmark links for historical results. Record the source and redistribution terms in `NOTICE` when adding third-party assets.

## Publishing

The `release.yml` GitHub Actions workflow runs on manual dispatch from a version tag such as `v2.0.0`. Configure a pending Trusted Publisher for `safety-gymnasium2` on each registry using this repository and workflow. Use the `testpypi` environment on TestPyPI and `pypi` on PyPI. The workflow checks the staged archives and smoke-tests their installed wheel before uploading the same archives to PyPI.

Credits: this contributing guide is based on the [PyTorch](https://github.com/pytorch/pytorch/) one.
