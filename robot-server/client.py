#!/usr/bin/env python3

import socket
import time

from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, MoveSteering, SpeedPercent)
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, ColorSensor
from ev3dev2.sound import Sound

from simple_pid import PID


from RobotCommunicator import RobotCommunicatorClient
import time

HOST = '10.42.0.1'
PORT = 65530

is_automatic = False 
is_move_forward = False
square_center_position = (0, 0)

rotate_angle_factor = 1.56
max_distance_us = 100

previous_position = 0

steer_speed = SpeedPercent(40)
gyro_offset = 6
cumulative_angle = 0


def move_forward(speed, motors):
    motors.on(0, speed)

    global previous_position, cumulative_angle
    if (speed == 0):
        travelled_angle = left_motor.position - previous_position
        travelled_distance = (travelled_angle / 360) * (3.14159 * 5.6)
        robot_comm.send_message({"command": "update_map", "distance": travelled_distance, "angle": cumulative_angle})
        motors.gyro.reset()
        cumulative_angle = 0
    else:
        previous_position = left_motor.position


def move_forward_distance(speed, distance, motors):
    global cumulative_angle
    motors.on_for_rotations(0, speed, distance / (3.14 * 5.6))
    robot_comm.send_message({"command": "update_map", "distance": distance, "angle": cumulative_angle})
    motors.gyro.reset()
    cumulative_angle = 0

def steer(angle, motors):
    motors.gyro.reset()

    direction = -1 if angle > 0 else 1
    motors.on(100 * direction, steer_speed)

    while abs(motors.gyro.angle) + gyro_offset <= abs(angle):
        continue

    motors.on(0, 0)

    time.sleep(0.5)

    global cumulative_angle
    cumulative_angle += motors.gyro.angle
    print("Rotated. Cumulative Angle: ", cumulative_angle)

def check_for_item():
    if color_sensor.color == ColorSensor.COLOR_RED:
        motors.off()
        move_forward_distance(-5, 2, motors)
        sound.beep()
        claw.on_for_rotations(60, 3)
        return True

if __name__ == "__main__":

    robot_comm=RobotCommunicatorClient(HOST, PORT)
    motors=MoveSteering(OUTPUT_B, OUTPUT_C, motor_class=LargeMotor)
    motors.gyro=GyroSensor()
    motors.gyro.calibrate()
    left_motor=LargeMotor(OUTPUT_B)
    right_motor=LargeMotor(OUTPUT_C)
    color_sensor=ColorSensor()
    claw=MediumMotor(OUTPUT_D)
    sound=Sound()
    robot_comm.start()
    current_location = (0, 0)
    sound.beep()
    iteration=0
    has_anything_in_claw = False

    while True:

        msg=robot_comm.pop_message()

        if has_anything_in_claw:
            travelled_angle = left_motor.position - previous_position
            travelled_distance = (travelled_angle / 360) * (3.14159 * 5.6)
            robot_comm.send_message({"command": "grabbed_item", "distance": travelled_distance, "angle": cumulative_angle, "sender": 0})
            is_automatic = False
            has_anything_in_claw = False

        if is_automatic:
            has_anything_in_claw = check_for_item()
            if has_anything_in_claw: continue

            direction = 1
            move_forward_distance(25, 80, motors)

            has_anything_in_claw = check_for_item()
            if has_anything_in_claw: continue

            steer(90 * (1 if iteration % 2 == 0 else -1) * direction,  motors)

            has_anything_in_claw = check_for_item()
            if has_anything_in_claw: continue

            move_forward_distance(25, 10, motors)

            has_anything_in_claw = check_for_item()
            if has_anything_in_claw: continue


            steer(90 * (1 if iteration % 2 == 0 else -1) * direction,  motors)

            iteration = iteration + 1
            if iteration > 10:
                iteration = 0
                direction = direction * 1


        if not msg:
            continue

        command=msg.get("command")
        print("Received command: ", command)

        if command == "move_forward":
            is_automatic = False
            move_forward(msg.get("speed"), motors)

        elif command == "move_forward_distance":
            is_automatic = False
            move_forward_distance(msg.get("speed"), msg.get("distance"), motors)
            robot_comm.send_message({"distance": msg.get("distance"), "angle": cumulative_angle})
            motors.gyro.reset()
            cumulative_angle = 0

        elif command == "rotate":
            is_automatic = False
            steer(msg.get("angle"), motors)

        elif command == "beep":
            sound.beep()

        elif command == "claw":
            is_automatic = False
            grab=msg.get("grab")
            claw.on_for_rotations(100 if grab else -100, 1)

        elif command == "automatic":
            is_automatic = msg.get("automatic")
            square_center_position = msg.get("position")
            previous_position = left_motor.position
            print("SQUARE CENTER POSITION: " + str(square_center_position))

        elif command == "go_origin":
            sound.beep()

            rot_ang = abs(msg.get("angle")) % 360

            if (msg.get("angle") < 0):
                rot_ang *= -1
            
            steer(rot_ang, motors)
            print("Rotating for: ", rot_ang, "Cumulative angle: ", cumulative_angle)
            move_forward_distance(40, msg.get("distance"), motors)
            robot_comm.send_message({"distance": msg.get("distance"), "angle": cumulative_angle})
            motors.gyro.reset()
            cumulative_angle = 0

        elif command == "drop_item":
            claw.on_for_rotations(60, -5)
            has_anything_in_claw = False

        elif command == "give_location":
            current_location = msg.get("location")
            print("Current location: ", current_location)
        
        elif command == "shutdown":
            motors.stop()
            break

    motors.off()
