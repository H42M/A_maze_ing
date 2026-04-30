PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
MAIN ?= a_maze_ing.py
CONFIG ?= config.txt

PY_FILES := a_maze_ing.py \
	config_parsing.py \
	maze_config.py \
	maze_generator.py \
	maze_solver.py \
	maze_terminal.py

# 	PY_FILES := $(shell git ls-files '*.py')

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	
	@if [ ! -d ".venv" ]; then \
		echo "No virtual environment found, please run: make install"; \
		exit 1; \
	else \
		.venv/bin/python $(MAIN) $(CONFIG); \
	fi
	
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
	rm -rf .venv

lint:
	flake8 $(PY_FILES)
	mypy $(PY_FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 $(PY_FILES)
	mypy $(PY_FILES) --strict