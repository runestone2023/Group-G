SHELL=/bin/bash
VENV_NAME=.venv
PYTHON=${VENV_NAME}/bin/python3
PIP=${VENV_NAME}/bin/pip3
ROBOT_IP=10.42.0.3

init:
	python -m venv .venv
	make requirements

requirements:
	${PIP} install -r requirements.txt

server:
	cd ./robot-server && ../${PYTHON} -m uvicorn server:app --reload

client:
	@scp -r ./robot-server/*.py robot@${ROBOT_IP}:~/
	@ssh robot@${ROBOT_IP} '~/client.py && pkill python'
