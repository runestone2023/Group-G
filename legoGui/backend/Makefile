SHELL=/bin/bash
VENV_NAME=.venv
PYTHON=${VENV_NAME}/bin/python3
PIP=${VENV_NAME}/bin/pip3

init:
	python -m venv .venv
	make requirements

requirements:
	${PIP} install -r requirements.txt

server:
	${PYTHON} -m uvicorn server:app --reload

client:
	./client.py