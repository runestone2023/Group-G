#!/usr/bin/env pybricks-micropython from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import socket
import selectors
import types
import json
from service_connection import service_connection

HOST = '127.0.0.1'
PORT = 65530

def main():
    # Create your objects here.
    # ev3 = EV3Brick()

    # Write your program here.
    # ev3.speaker.beep()

    sel = selectors.DefaultSelector()
    send_queue = []
    recv_queue = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to", HOST, PORT)
        s.connect((HOST, PORT))
        s.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        data = types.SimpleNamespace(addr=s.getsockname(), inb=b"", outb=b"")
        sel.register(s, events, data=data)

        while True:
            events = sel.select(timeout=10)
            for key, mask in events:
                if key.data is not None:
                    service_connection(
                        key, mask, sel, send_queue, recv_queue)
        
            if len(recv_queue) > 0:
               handle_message(recv_queue.pop(0), send_queue)

def handle_message(message, send_queue):
    print(message)

if __name__ == "__main__":
    main()
