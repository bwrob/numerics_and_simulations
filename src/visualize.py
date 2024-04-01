"""Visualize module."""

from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.cm import rainbow

def animate_data(data: List[Tuple[float, float]], *, title: str = "") -> None:
    """Animate scatter plot of data points."""
    x, y = zip(*data)
    colors = rainbow(np.linspace(0, 1, len(y)))

    fig, ax = plt.subplots()
    if title:
        ax.set_title(title)
    ax.set_xlim(0, 2)
    ax.set_ylim(-1, 1)
    ax.grid(True)
    ax.set_aspect("equal")

    graph = ax.scatter([], [])

    def update(frame: int) -> None:
        """Update scatter plot with new data points."""
        graph.set_offsets(np.column_stack((x[: frame + 1], y[: frame + 1])))
        graph.set_facecolors(colors[: frame + 1])

    _ = FuncAnimation(fig, update, frames=len(y), repeat=False)
    plt.show()
