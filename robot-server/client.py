#!/usr/bin/env python3

import socket
import time

from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, MoveSteering, SpeedPercent)
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor
from ev3dev2.sound import Sound

from simple_pid import PID


from RobotCommunicator import RobotCommunicatorClient
import time

HOST = '192.168.0.3'
PORT = 65530

rotate_angle_factor = 2.39
max_distance_us = 100

steer_speed = SpeedPercent(40)
gyro_offset = 10


class AngleLearner:
    def __init__(self):
        self.angle = 45

    def update(self, sensor_offset):
        # global steer_speed
        # steer_speed = SpeedPercent(rotation_speed)
        global gyro_offset
        gyro_offset = sensor_offset
        steer(self.angle, motors)
        return motors.gyro.angle


def move_forward(speed, motors):
    motors.on(0, speed)

def move_forward_distance(speed, distance, motors):
    motors.on_for_rotations(0, speed, distance / (3.14 * 5.6))

def steer(angle, motors):
    motors.gyro.reset()

    direction = -1 if angle > 0 else 1
    motors.on(100 * direction, steer_speed)

    while abs(motors.gyro.angle) + gyro_offset <= abs(angle):
        continue

    motors.on(0, 0)

    time.sleep(0.5)

def learn_angle_pid(iterations):
    angle_learner = AngleLearner()


    motors.gyro.reset()

    
    original_offset = gyro_offset

    pid = PID(0.5, 0.01, 0.2, setpoint=angle_learner.angle)

    # pid.output_limits = (-40, 5)

    steer(angle_learner.angle, motors)
    current_angle = motors.gyro.angle

    print("Starting angle: ", current_angle)

    iter = 0
    while iter < iterations:
        print("Iteration: ", iter)
        sensor_offset = pid(abs(current_angle))
        gyro_o = original_offset - sensor_offset
        # if abs(rotation_speed) == 0:
        #     rotation_speed = 2
        # elif abs(rotation_speed) < 2:
        #     rotation_speed = 2 * (rotation_speed / abs(rotation_speed))
        # elif abs(rotation_speed) > 100:
        #     rotation_speed = 100 * (rotation_speed / abs(rotation_speed))
        current_angle = angle_learner.update(gyro_o)
        print("Current Angle:", current_angle,"gyro offset: ", gyro_o , "sensor offset: ", sensor_offset)
        if (abs(abs(current_angle) - abs(angle_learner.angle)) < 2):
            break
        iter += 1
    
    print(current_angle, gyro_o)


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
        print("Received command: ", command)
        if command == "move_forward":
            # if msg.get("speed") == 0:
            #     print("Travelled distance", ((motors.position - initial_position) / 360) * ())
            # else:
            #     initial_position = motors.position
            move_forward(msg.get("speed"), motors)

        elif command == "move_forward_distance":
            move_forward_distance(msg.get("speed"), msg.get("distance"), motors)
            robot_comm.send_message({"distance": msg.get("distance"), "angle": motors.gyro.angle})
            motors.gyro.reset()

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

        elif command == "learn_angle":
            print("Learning angle")
            learn_angle_pid(msg.get("iters"))       

        elif command == "shutdown":
            motors.stop()
            break

    motors.off()
