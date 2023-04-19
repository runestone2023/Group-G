#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import socket               
import json

# Create your objects here.
ev3 = EV3Brick()

# Write your program here.
ev3.speaker.beep()
# hook = Motor(Port.A)

# while True:
#     hook.run(700)
#     wait(2000)
#     hook.run(-700)
#     wait(2000)

s = socket.socket()         
port = 65530                
s.connect(('10.42.0.1', port))

obj = { 'test' : 30,
       'test1' : 31 }
body = json.dumps(obj).encode('utf-8')
print(body)
message_length = len(body)
print(message_length)

s.send(message_length.to_bytes(2, 'big'))
s.send(body)

s.close()          
