from math import cos, sin

class Observation:
    """
    Class to represent an observation from the robot's sensors.
    """

    def __init__(self, distance, angle, type, color):
        self.distance = distance
        self.angle = angle
        self.type = type
        self.color = color

    # Code to get x and y coordinates from distance and angle
    def get_x(self):
        return self.distance * cos(self.angle)

    def get_y(self):
        return self.distance * sin(self.angle)
    