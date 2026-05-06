install:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

debug:
	.venv/bin/python -m pdb a_maze_ing.py

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

lint-doc:
	flake8 . --exclude=.venv,.env --extend-ignore=D100,D101,D102,D103,D104
	mypy . --exclude '\.venv|\.env' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	make clean


run: install
	.venv/bin/python a_maze_ing.py config.txt
	make clean