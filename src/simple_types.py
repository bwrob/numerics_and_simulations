"""Types for the simple functions."""

from collections import namedtuple

RootFindingData = namedtuple(
    "RootFindingData", ["value", "iteration_no", "iteration_points"]
)
