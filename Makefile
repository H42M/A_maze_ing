PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
MAIN ?= a_maze_ing.py
CONFIG ?= config.txt

PY_FILES := a_maze_ing.py \
	config_parsing.py \
	maze_config.py \
	maze_generator.py \
	maze_terminal.py

# 	PY_FILES := $(shell git ls-files '*.py')

.PHONY: install run debug clean lint lint-strict

install:
	$(PIP) install -r requirements.txt
	$(PIP) install flake8 mypy

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

lint:
	flake8 $(PY_FILES)
	mypy $(PY_FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 $(PY_FILES)
	mypy $(PY_FILES) --strict