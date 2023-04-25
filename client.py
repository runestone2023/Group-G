#!/usr/bin/env python3
# from ev3dev2.sound import Sound
from RobotCommunicator import RobotCommunicatorClient
import time

HOST = '10.42.0.1'
PORT = 65530

def main():
    # Create your objects here.
    # sound = Sound()
    # sound.beep()

    robot_comm = RobotCommunicatorClient(HOST, PORT)
    res = robot_comm.send_message({"tesing": "testing"})

    while True:
        time.sleep(2)


if __name__ == "__main__":
    main()
