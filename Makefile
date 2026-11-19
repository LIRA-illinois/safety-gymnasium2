UV ?= uv
PROJECT_PATH = safety_gymnasium2
SOURCE_FOLDERS = $(PROJECT_PATH) examples tests docs
TEST_EXTRAS = --extra racing --extra building
PYTESTOPTS ?=

.PHONY: default install install-editable install-e uninstall build pytest test lint ruff ruff-fix \
        pylint flake8 py-format pre-commit mypy type format addlicense docs docs-build \
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

pytest:
	$(UV) run --locked --group test $(TEST_EXTRAS) pytest tests $(PYTESTOPTS) \
		--cov=$(PROJECT_PATH) --cov-config=tests/.coveragerc \
		--cov-report=term-missing --cov-report=xml:tests/coverage.xml

test: pytest

ruff:
	$(UV) run --locked --group lint ruff check $(SOURCE_FOLDERS)

ruff-fix:
	$(UV) run --locked --group lint ruff check --fix $(SOURCE_FOLDERS)

pylint:
	$(UV) run --locked --group lint pylint $(PROJECT_PATH)

flake8:
	$(UV) run --locked --group lint flake8 --count --show-source --statistics $(SOURCE_FOLDERS)

py-format:
	$(UV) run --locked --group lint isort --check $(SOURCE_FOLDERS)
	$(UV) run --locked --group lint black --check $(SOURCE_FOLDERS)

format:
	$(UV) run --locked --group lint isort $(SOURCE_FOLDERS)
	$(UV) run --locked --group lint black $(SOURCE_FOLDERS)

pre-commit:
	$(UV) run --locked --group lint pre-commit run --all-files

mypy:
	$(UV) run --locked --group lint mypy $(PROJECT_PATH)

type:
	$(UV) run --locked --group lint ty check $(PROJECT_PATH)

lint: ruff flake8 py-format pylint

commit-checks: lint type

addlicense:
	go run github.com/google/addlicense@latest -check -l apache $(SOURCE_FOLDERS)

docs:
	$(UV) run --locked --group docs sphinx-autobuild --watch $(PROJECT_PATH) docs docs/_build/html

docs-build:
	$(UV) run --locked --group docs sphinx-build -W -b html docs docs/_build/html

docstyle:
	$(UV) run --locked --group lint doc8 docs

spelling:
	$(UV) run --locked --group docs sphinx-build -t spelling -b spelling docs docs/_build/spelling

clean-docs:
	rm -rf docs/_build

clean-py:
	find $(SOURCE_FOLDERS) -depth -type d -name __pycache__ -exec rm -r '{}' +

clean-build:
	rm -rf build dist *.egg-info

clean: clean-py clean-build clean-docs
