#!/usr/bin/env python

import _thread
from fastapi import FastAPI
from RobotCommunicator import RobotCommunicatorServer
from models import MoveCmd, RotateCmd

PORT = 65530

app = FastAPI()
robot_server = RobotCommunicatorServer('', PORT)
robot_server.start()


@app.get("/clients")
async def clients():
    return robot_server.list_clients()

@app.post("/clients/{client_id}/shutdown")
async def shutdown(client_id):
    res = robot_server.send_message({'command': 'shutdown'}, client_id)
    return {"client_id": client_id, 'move_forward': res}


@app.post("/clients/{client_id}/move")
async def send_move(client_id: int, body: MoveCmd):
    res = robot_server.send_message(
        {'command': 'move_forward', 'speed': body.speed, 'distance': body.distance}, client_id)
    return {"client_id": client_id, 'move_forward': res}


@app.post("/clients/{client_id}/rotate")
async def send_rotate(client_id: int, body: RotateCmd):
    res = robot_server.send_message(
        {'command': 'rotate', 'angle': body.angle}, client_id)
    return {"client_id": client_id, 'move_forward': res}
