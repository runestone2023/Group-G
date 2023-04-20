#!/usr/bin/env python

import _thread
import uvicorn
from fastapi import FastAPI
from server import robot_server

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def handle_robot_msg(message):
    print(message)


if __name__ == "__main__":
    send_queue = []
    tid = _thread.start_new_thread(
        robot_server, (send_queue, handle_robot_msg))

    uvicorn.run(
        'main:app',
        host="0.0.0.0",
        port=80,
        log_level="debug",
    )
