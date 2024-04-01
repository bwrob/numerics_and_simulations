import collections
import time

import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np


# decorator for debugging purposes
# debug - gather debugging info during computation:
#   y   full
#   n   none
# value - output result only rather than named tuple with auxiliary data:
#   y   value
#   n   all data
# best to use with default control so that the settings for all functions can be switched at once
def debugging(control="yny"):
    debug, value, timer = control

    def wrapper(f):
        def wrapped(*args, **kwargs):
            if timer == "y":
                tic = time.perf_counter()
            result = f(debug, *args, **kwargs)
            if timer == "y":
                toc = time.perf_counter()
                print("{} evaluated in {} seconds".format(f.__name__, toc - tic))

            if value == "y":
                try:
                    return result.value
                except AttributeError:
                    print("Failed in {}".format(f.__name__))
            else:
                return result

        return wrapped

    return wrapper


# named tuple for root-finding output
RootFindingData = collections.namedtuple(
    "RootFindingData", ["value", "iteration_no", "iteration_points"]
)


# animate points on plot
def animate(data):
    x, y = [point[0] for point in data], [point[1] for point in data]
    colors = cm.rainbow(np.linspace(0, 1, len(y)))
    fig = plt.figure()
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    graph = plt.scatter([], [])

    def animate(i):
        graph.set_offsets(np.vstack((x[: i + 1], y[: i + 1])).T)
        graph.set_facecolors(colors[: i + 1])
        return graph

    ani = animation.FuncAnimation(fig, animate, repeat=False, interval=200)
    plt.show()
