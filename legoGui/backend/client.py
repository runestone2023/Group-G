# #!/usr/bin/env python3
# import socket

# import config
# from ev3dev2.motor import (OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
#                            MediumMotor, MoveSteering)
# from ev3dev2.sensor.lego import UltrasonicSensor
# from ev3dev2.sound import Sound


# from RobotCommunicator import RobotCommunicatorClient
# import time

# HOST = '10.42.0.1'
# PORT = 65530

# SOUND_ON = False
# sound = Sound()

# recv_buffer = b""
# end_char = b"\0"

# angle_to_distance_factor = 36
# rotate_angle_factor = 5.56
# sensor_rotation_multiplier = 3
# max_sensor_read_distance = 50

# robot_comm = RobotCommunicatorClient(HOST, PORT)
# res = robot_comm.send_message({"tesing": "testing"})
# print(res)
# time.sleep(1)

# def say(msg):
#     if SOUND_ON:
#         sound.speak(msg)
#     print(msg)

# # Initialize the motors
# steering_motors = MoveSteering(OUTPUT_B, OUTPUT_C, motor_class=LargeMotor)
# sensor_rotation_motor = MediumMotor(OUTPUT_D)

# # Initialize the ultrasonic sensor
# us_sensor = UltrasonicSensor()
# sensor_orientation = 0

# # Functions to move forward
# def move_forward(speed):
#     steering_motors.on_for_rotations(speed=speed)

# def move_forward(speed, distance):
#     steering_motors.on_for_rotations(steering=0, speed=speed, degrees=distance*angle_to_distance_factor)

# # Functions to rotate
# def rotate(angle):
#     steering_motors.on_for_rotations(steering=-100, speed=30, degrees=rotate_angle_factor * angle)

# def rotate_sensor(angle):
#     sensor_rotation_motor.on_for_rotations(speed=5, degrees=sensor_rotation_multiplier * angle, block=True)
#     global sensor_orientation
#     sensor_orientation += sensor_rotation_multiplier * angle

# def reset_sensor_rotation():
#     rotate_sensor(-sensor_orientation / sensor_rotation_multiplier, speed=20)

# # Functions to read sensor

# def read_sensor(angle):
#     m = us_sensor.distance_centimeters
#     if m <= max_sensor_read_distance:
#         reading = {"distance": m, "orientation": angle, 'type': 'obs'}
#     else:
#         reading = {"distance": m, "orientation": angle, 'type': 'free'}
#     return reading

# def read_send_sensor(angle):
#     reading = read_sensor(angle)
#     robot_comm.send_message(reading)
#     print(reading)
#     time.sleep(1)

# def scan(interval, num_scans, clockwise=True):
#     robot_comm.send_message({"action": "scan_start"})
#     rotation_angle = (interval - 1) * num_scans

#     if clockwise:
#         rotation_angle *= -1

#     start_pos = sensor_rotation_motor.position
#     next_scan_pos = 0

#     rotate_sensor(rotation_angle)

#     while sensor_rotation_motor.is_running:
#         current_relative_rotation = sensor_rotation_motor.position - start_pos
#         if (current_relative_rotation / sensor_rotation_multiplier) >= next_scan_pos:
#             read_send_sensor(next_scan_pos)
#             next_scan_pos += interval
    
#     if next_scan_pos <= rotation_angle:
#         read_send_sensor(rotation_angle)

#     robot_comm.send_message({"action": "scan_end"})
    


# if __name__ == "__main__":

#     # Main Robot Loop
#     while True:
#         msg = robot_comm.pop_message()
#         if not msg:
#             pass
#         command = msg.get("command")
#         if command == "move_forward":
#             move_forward(msg.get("speed"), msg.get("distance"))
#         elif command == "rotate":
#             rotate(msg.get("angle"))
#         elif command == "scan":
#             scan(msg.get("interval"), msg.get("num_scans"), msg.get("clockwise"))
#         elif command == "reset_sensor_rotation":
#             reset_sensor_rotation()
#         elif command == "rotate_sensor":
#             rotate_sensor(msg.get("angle"))
#         elif command == "shut_down":
#             break
#         else:
#             print("Unknown command: {}".format(command))

#     say("Shutting Down")
#     reset_sensor_rotation()
#     steering_motors.off()
#     sensor_rotation_motor.off()
        

