import _thread
import uvicorn
from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from RobotCommunicatorServer import RobotCommunicatorServer



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
    result = [{
        "clientID" : "1",
        "robot" : "SWE1"
    }]
    # return robot_server.list_clients()
    return result


@app.post("/start")
async def start():
    result = {}
    for client_id in robot_server.list_clients():
        result[client_id] = robot_server.send_message(
            {"op": "start"}, client_id)
    

    print("In Uvicorn terminal start() called")
    # i set result to the string , to check if the ui can call this function
    #  delete the next link to return correct "result"
    result = "def start() called"
    return result


@app.post("/stop")
async def stop():
    result = {}
    for client_id in robot_server.list_clients():
        result[client_id] = robot_server.send_message(
            {"op": "start"}, client_id)
        
    print("In Uvicorn terminal stop() called")
    # i set "result" to the string , to check if the ui can call this function.
    #  delete the next link to return correct "result"
    result = "def stop() called"
    return result

