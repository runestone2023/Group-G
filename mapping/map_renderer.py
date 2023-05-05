from observation import Observation
from enums import ObservationType
import matplotlib.pyplot as plt

class MapRenderer:
    """
    Renders the map.
    """
    def __init__(self, map) -> None:
        self.map = map

    def render(self, map):
        pixels = [[0 if map[x][y].type == ObservationType.FREE else 1 for x in range(map.width)] for y in range(map.height)]
        plt.imshow(map, interpolation='nearest')
        plt.show()

