#!/usr/bin/env python3

import socket
import time

from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, MoveSteering, SpeedPercent)
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor
from ev3dev2.sound import Sound


from RobotCommunicator import RobotCommunicatorClient
import time

HOST = '10.42.0.1'
PORT = 65530

def move_forward(speed, motors):
    motors.on(0, speed)


def steer(angle, motors):
    motors.gyro.reset()

    direction = -1 if angle > 0 else 1
    motors.on(100 * direction, SpeedPercent(20))

    while abs(motors.gyro.angle) + 10 <= abs(angle):
        continue

    motors.on(0, 0)


if __name__ == "__main__":
    robot_comm=RobotCommunicatorClient(HOST, PORT)
    motors=MoveSteering(OUTPUT_B, OUTPUT_C, motor_class=LargeMotor)
    motors.gyro=GyroSensor()
    motors.gyro.calibrate()

    claw=MediumMotor(OUTPUT_D)

    sound=Sound()

    robot_comm.start()

    sound.beep()
    while True:
        msg=robot_comm.pop_message()
        if not msg:
            continue

        command=msg.get("command")
        if command == "move_forward":
            move_forward(msg.get("speed"), motors)

        elif command == "rotate":
            steer(msg.get("angle"), motors)

        elif command == "beep":
            sound.beep()

        elif command == "claw":
            grab=msg.get("grab")
            claw.on_for_rotations(100 if grab else -100, 1)

        elif command == "scan":
            us = UltrasonicSensor()
            distance = us.distance_centimeters
            obj_type = "obs" if distance <= max_distance_us else "free"
            robot_comm.send_message({"distance": distance, "type": obj_type})

        elif command == "shut_down":
            motors.stop()
            break

    motors.off()
