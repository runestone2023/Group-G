from mapping.observation import Observation
from mapping.enums import ObservationType
import matplotlib.pyplot as plt
import io
import base64

class MapRenderer:
    """
    Renders the map.
    """
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width

    def render(self, observations, robot_path):
        # Initialize the plot
        fig, ax = plt.subplots()
        ax.set_xlim(-self.width, self.width)
        ax.set_ylim(-self.height, self.height)
        ax.axvline(x=0, c="green", label="x=0")
        ax.axhline(y=0, c="green", label="y=0")
        ax.set_aspect('equal')

        # Plot the coordinates
        for coordinate in observations:
            if coordinate.type == ObservationType.OBS:
                ax.scatter(coordinate.get_x(), coordinate.get_y(), color='black')
            elif coordinate.type == ObservationType.FREE:
                ax.scatter(coordinate.get_x(), coordinate.get_y(), color='white')
            elif coordinate.type == ObservationType.UNKNOWN:
                ax.scatter(coordinate.get_x(), coordinate.get_y(), color='gray')

        # Plot the robot path
        ax.plot([c[0] for c in robot_path], [c[1] for c in robot_path], color='red')

        # Plot the robot
        ax.scatter(robot_path[-1][0], robot_path[-1][1], color='blue')

        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        return base64.b64encode(img_bytes.read())
