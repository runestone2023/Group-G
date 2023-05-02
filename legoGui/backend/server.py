import _thread
import uvicorn
from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from RobotCommunicator import RobotCommunicatorServer
from models import MoveCmd, RotateCmd, ClawCmd
import time


app = FastAPI()
origins = ['https://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ["*"]
)

IP = ''
PORT = 65530

robot_server = RobotCommunicatorServer(IP, PORT)
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



# @app.get("/clients")
# async def clients():
#     result = [{
#         "clientID" : "1",
#         "robot" : "SWE1"
#     }]
#     # return robot_server.list_clients()
#     return result

# @app.post("/start")
# async def start():
#     result = {}
#     for client_id in robot_server.list_clients():
#         result[client_id] = robot_server.send_message(
#             {"op": "start"}, client_id)
    

#     print("In Uvicorn terminal start() called")
#     # i set result to the string , to check if the ui can call this function
#     #  delete the next link to return correct "result"
#     result = "def start() called"
#     return result


# @app.post("/stop")
# async def stop():
#     result = {}
#     for client_id in robot_server.list_clients():
#         result[client_id] = robot_server.send_message(
#             {"op": "start"}, client_id)
        
#     print("In Uvicorn terminal stop() called")
#     # i set "result" to the string , to check if the ui can call this function.
#     #  delete the next link to return correct "result"
#     result = "def stop() called"
#     return result

