#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from RobotCommunicator import RobotCommunicatorClient
import time

HOST = '10.42.0.1'
PORT = 65530


def main():
    # Create your objects here.
    ev3 = EV3Brick()

    # Write your program here.
    ev3.speaker.beep()

    robot_comm = RobotCommunicatorClient(HOST, PORT)
    res = robot_comm.send_message({"tesing": "testing"})
    print(res)
    time.sleep(1)


if __name__ == "__main__":
    main()
