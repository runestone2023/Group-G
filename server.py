#!/usr/bin/env python

import _thread
import time
from fastapi import FastAPI
from RobotCommunicator import RobotCommunicatorServer
from models import MoveCmd, RotateCmd, ClawCmd, LearnCmd

PORT = 65530

app = FastAPI()
robot_server = RobotCommunicatorServer('', PORT)
robot_server.start()


@app.get("/clients")
async def clients():
    return robot_server.list_clients()


@app.post("/clients/{client_id}/shutdown")
async def shutdown(client_id: int):
    res = robot_server.send_message({'command': 'shutdown'}, client_id)
    return {"client_id": client_id, 'shutdown': res}


@app.post("/clients/{client_id}/move")
async def send_move(client_id: int, body: MoveCmd):
    res = robot_server.send_message(
        {'command': 'move_forward', 'speed': body.speed}, client_id)
    return {"client_id": client_id, 'move_forward': res}

@app.post("/clients/{client_id}/rotate")
async def send_rotate(client_id: int, body: RotateCmd):
    res = robot_server.send_message(
        {'command': 'rotate', 'angle': body.angle}, client_id)
    return {"client_id": client_id, 'rotate': res}


@app.post("/clients/{client_id}/beep")
async def send_beep(client_id: int):
    res = robot_server.send_message(
        {'command': 'beep'}, client_id)
    return {"client_id": client_id, 'beep': res}

@app.post("/clients/{client_id}/claw")
async def send_claw(client_id: int, body: ClawCmd ):
    res = robot_server.send_message(
            {'command': 'claw', 'grab' : body.grab}, client_id)
    return {"client_id": client_id, 'beep': res}

@app.post("/clients/{client_id}/scan")
async def send_scan(client_id: int):
    res = robot_server.send_message(
            {'command': 'scan'}, client_id)
    return {"client_id": client_id, 'scan_result': res}

@app.post("/clients/{client_id}/learn")
async def send_learn(client_id: int, body: LearnCmd):
    res = robot_server.send_message(
            {'command': 'learn_angle', 'iters': body.iters}, client_id)
    return {"client_id": client_id, 'learn_result': res}
