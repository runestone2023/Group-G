#!/usr/bin/env python3

import socket
import time

from ev3dev2.motor import (OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, MoveSteering)
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound


from RobotCommunicator import RobotCommunicatorClient
import time

HOST = '10.42.0.1'
PORT = 65530
rotate_angle_factor = 2.39


def move_forward(speed):
    steering_motors.on(0, speed)


def steer(angle):
    steering_motors.on_for_degrees(-100, 30, rotate_angle_factor * angle)


if __name__ == "__main__":
    robot_comm = RobotCommunicatorClient(HOST, PORT)
    steering_motors = MoveSteering(OUTPUT_B, OUTPUT_C, motor_class=LargeMotor)

    sound = Sound()

    robot_comm.start()

    sound.beep()
    while True:
        msg = robot_comm.pop_message()
        if not msg:
            continue

        print(msg)
        command = msg.get("command")
        if command == "move_forward":
            move_forward(msg.get("speed"))

        elif command == "rotate":
            steer(msg.get("angle"))

        elif command == "beep":
            sound.beep()

        elif command == "shut_down":
            break

    steering_motors.off()
