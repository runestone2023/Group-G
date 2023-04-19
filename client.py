#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import socket               

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

print(ev3)
s = socket.socket()         
port = 65530                
s.connect(('10.42.0.1', port))
print(s.recv(1024))
print(s.send(1024))
s.close()          