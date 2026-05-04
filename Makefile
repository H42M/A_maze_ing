build:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +

fclean:
	make clean
	rm output.txt
	rm -rf .venv

lint:
	flake8 . --exclude=.venv,.env
	mypy . --exclude '\.venv|\.env' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	make clean

lint-strict:
	flake8 . --exclude=.venv,.env
	mypy . --exclude '\.venv|\.env' --strict
	make clean

run: build
	.venv/bin/python pygame_maze.py
	make clean

run-terminal: build
	.venv/bin/python terminal_maze.py
	make clean