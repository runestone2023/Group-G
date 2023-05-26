from math import cos, sin, radians
from mapping.observation import Observation
from mapping.enums import ObservationType

class Map:
    """
    Class to represent the map of the environment.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_location = (0, 0)
        self.robot_path = [self.current_location]

    def add_observation(self, observation):
        self.map[self.current_location[0] + observation.get_x()][self.current_location[1] + observation.get_y()] = observation

    def update_current_location(self, distance, angle):
        self.current_location = (distance * cos(radians(angle)) + self.current_location[0], distance * sin(radians(angle)) + self.current_location[1])
        self.robot_path.append(self.current_location)

    