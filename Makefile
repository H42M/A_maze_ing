build:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

clean:
	rm -rf *__pycache__*
	rm -rf */*__pycache__*
	rm -rf */*/*__pycache__*

fclean:
	make clean
	rm -rf .venv

run: build
	.venv/bin/python main.py
	make clean