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

maps = {}
cumulative_angle: dict[int, int] = {}

def add_map_hook(id):
    maps[id] = Map(500, 500)
    cumulative_angle[id] = 0

robot_server.register_on_connect(add_map_hook)
map_renderer = MapRenderer(500, 500)
robot_server.start()

# Event loop for communicatimg with robots
while True:
    msg = robot_server.pop_message()
    time.sleep(0.05)

    if not msg:
        continue

    command = msg.get("command")
    command = msg.get("sender")

    # if command == ..


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
async def send_move_distance(client_id: int, body: MoveDistCmd):
    res = robot_server.send_message(
        {'command': 'move_forward_distance', 'speed': body.speed, 'distance': body.distance}, client_id)
    while robot_server._recv_messages == []:
        print("Waiting for answer")
        pass
    res = robot_server._recv_messages.pop(0)

    global cumulative_angle
    cumulative_angle += res['angle']

    if body.speed < 0:
        res['distance'] *= -1

    maps[client_id].update_current_location(res['distance'], cumulative_angle[client_id])
    print("Current location: ", maps[client_id].current_location)

    
    return {"client_id": client_id, 'move_forward_distance': res}

@app.get("/clients/{client_id}/map")
async def get_map(client_id: int):
    png = map_renderer.render([], maps[client_id].robot_path)
    return { "image": png }

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
