from observation import Observation
from enums import ObservationType

class Map:
    """
    Class to represent the map of the environment.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[Observation(-1, -1, ObservationType.UNKNOWN) for x in range(width)] for y in range(height)]
        self.current_location = (0, 0)

    def add_observation(self, observation):
        self.map[self.current_location[0] + observation.get_x()][self.current_location[1] + observation.get_y()] = observation


    