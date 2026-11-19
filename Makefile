UV ?= uv
PROJECT_PATH = safety_gymnasium2
SOURCE_FOLDERS = $(PROJECT_PATH) examples tests docs asset_packs
COMPATIBILITY_PATHS = $(PROJECT_PATH)/utils/registration.py $(PROJECT_PATH)/assets/paths.py \
                      $(PROJECT_PATH)/vector $(PROJECT_PATH)/wrappers
FORMAT_PATHS = $(COMPATIBILITY_PATHS) examples tests docs asset_packs
TEST_EXTRAS = --extra racing --extra building
TESTOPTS ?=

.PHONY: default install install-editable install-e uninstall build test lint ruff ruff-fix \
        py-format pre-commit type type-compat format addlicense docs docs-build \
        docstyle spelling clean-docs clean-py clean-build clean commit-checks

default: install

install:
	$(UV) sync --locked --no-editable

install-editable:
	$(UV) sync --locked

install-e: install-editable

uninstall:
	$(UV) pip uninstall safety-gymnasium2

build:
	$(UV) build --all-packages --no-sources

test:
	$(UV) run --locked --group test $(TEST_EXTRAS) coverage run -m unittest discover \
		-s tests -p 'test_*.py' $(TESTOPTS)
	$(UV) run --locked --group test coverage report
	$(UV) run --locked --group test coverage xml

ruff:
	$(UV) run --locked --group lint ruff check $(SOURCE_FOLDERS)

ruff-fix:
	$(UV) run --locked --group lint ruff check --fix $(SOURCE_FOLDERS)

py-format:
	$(UV) run --locked --group lint ruff check --select I $(FORMAT_PATHS)
	$(UV) run --locked --group lint ruff format --check $(FORMAT_PATHS)

format:
	$(UV) run --locked --group lint ruff check --select I --fix $(FORMAT_PATHS)
	$(UV) run --locked --group lint ruff format $(FORMAT_PATHS)

pre-commit:
	$(UV) run --locked --group lint pre-commit run --all-files

type:
	$(UV) run --locked --group lint ty check $(PROJECT_PATH)

type-compat:
	$(UV) run --locked --group lint ty check $(COMPATIBILITY_PATHS)

lint: ruff py-format

commit-checks: lint type-compat

addlicense:
	go run github.com/google/addlicense@latest -check -l apache $(SOURCE_FOLDERS)

docs:
	$(UV) run --locked --group docs sphinx-autobuild --watch $(PROJECT_PATH) docs docs/_build/html

docs-build:
	$(UV) run --locked --group docs sphinx-build -W -b html docs docs/_build/html

docstyle:
	$(UV) run --locked --group docs doc8 docs

spelling:
	$(UV) run --locked --group docs sphinx-build -t spelling -b spelling docs docs/_build/spelling

clean-docs:
	rm -rf docs/_build

clean-py:
	find $(SOURCE_FOLDERS) -depth -type d -name __pycache__ -exec rm -r '{}' +

clean-build:
	rm -rf build dist *.egg-info

clean: clean-py clean-build clean-docs
