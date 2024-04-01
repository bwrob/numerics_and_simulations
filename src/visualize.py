"""Visualize module."""

from typing import List, Tuple

import matplotlib
import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np


def animate(data: List[Tuple[float, float]]) -> None:
    """
    Animate a scatter plot of data points.

    Parameters:
        data (List[Tuple[float, float]]): A list of tuples representing the x and y coordinates of the data points.

    Returns:
        None

    """
    x, y = [point[0] for point in data], [point[1] for point in data]
    colors = cm.rainbow(np.linspace(0, 1, len(y)))
    fig = plt.figure()
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    graph = plt.scatter([], [])

    def animate(i: int) -> matplotlib.collections.PathCollection:
        """
        Update the scatter plot with new data points.

        Parameters:
            i (int): The index of the data point to update.

        Returns:
            matplotlib.collections.PathCollection: The updated scatter plot.

        """
        graph.set_offsets(np.vstack((x[: i + 1], y[: i + 1])).T)
        graph.set_facecolors(colors[: i + 1])
        return graph

    ani = animation.FuncAnimation(fig, animate, repeat=False, interval=200)
    plt.show()
    plt.show()
