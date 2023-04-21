#!/usr/bin/env python

import _thread
import uvicorn
from fastapi import FastAPI
from RobotCommunicatorServer import RobotCommunicatorServer

app = FastAPI()
robot_server = RobotCommunicatorServer()
robot_server.start()

@app.get("/clients")
async def clients():
    return robot_server.list_clients()

@app.get("/start")
async def start():
    robot_server.send_message({"operation" : "start"}, 0)
    return {}

@app.get("/stop")
async def stop():
    robot_server.send_message({"operation" : "stop"}, 0)
    return {}
