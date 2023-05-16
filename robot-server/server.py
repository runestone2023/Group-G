#!/usr/bin/env python

import _thread
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from RobotCommunicator import RobotCommunicatorServer
from models import MoveCmd, RotateCmd, ClawCmd, LearnCmd, MoveDistCmd
from mapping import Map, Observation, MapRenderer

PORT = 65530

app = FastAPI()
# we need this middleware to communicate with the ui , as they are in different ports(3000 for ui & 8000 for backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ["*"]
)

robot_server = RobotCommunicatorServer('', PORT)
robot_server.start()

map = Map(500, 500)


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

@app.post("/clients/{client_id}/move_distance")
async def send_move(client_id: int, body: MoveDistCmd):
    res = robot_server.send_message(
        {'command': 'move_forward_distance', 'speed': body.speed, 'distance': body.distance}, client_id)
    while robot_server._recv_messages == []:
        print("Waiting for answer")
        pass
    res = robot_server._recv_messages.pop(0)

    if body.speed < 0:
        res['angle'] = 180 - res['angle']

    map.update_current_location(res['distance'], res['angle'])
    print("Current location: ", map.current_location)
    
    return {"client_id": client_id, 'move_forward_distance': res}

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
    while robot_server._recv_messages == []:
        print("Waiting for answer")
        pass
    res = robot_server._recv_messages.pop(0)
    return {"client_id": client_id, 'scan_result': res}

@app.post("/clients/{client_id}/learn")
async def send_learn(client_id: int, body: LearnCmd):
    res = robot_server.send_message(
            {'command': 'learn_angle', 'iters': body.iters}, client_id)
    return {"client_id": client_id, 'learn_result': res}
