install:
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .mypy_cache
	rm output.txt

run:
	./.venv/bin/python a_maze_ing.py config.txt
	make clean

lint:
	flake8 . --exclude=.venv,.env
	mypy . --exclude '\.venv|\.env' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --exclude=.venv,.env
	mypy . --exclude '\.venv|\.env' --strict