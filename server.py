#!/usr/bin/env python

import _thread
import uvicorn
from fastapi import FastAPI
from RobotCommunicator import RobotCommunicatorServer

IP = ''
PORT = 65530

app = FastAPI()
robot_server = RobotCommunicatorServer(IP, PORT)
robot_server.start()


@app.get("/clients")
async def clients():
    return robot_server.list_clients()


@app.post("/start")
async def start():
    result = {}
    for client_id in robot_server.list_clients():
        result[client_id] = robot_server.send_message(
            {"op": "start"}, client_id)
    return result


@app.post("/stop")
async def stop():
    result = {}
    for client_id in robot_server.list_clients():
        result[client_id] = robot_server.send_message(
            {"op": "start"}, client_id)
    return result
