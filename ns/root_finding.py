"""Root finding module."""

from math import sin
from typing import Callable, Final

from ns.simple_types import RootFindingData
from ns.utils import debug
from ns.visualize import animate_data

MAX_ITER = 999_999
D_STEP = 1e-6


@debug()
def root_newton(
    debug_: bool,
    f: Callable[[float], float],
    start_point: float,
    epsilon: float,
    h: float = D_STEP,
) -> RootFindingData:
    """
    Finds the root of a function using the Newton's method.

    Args:
        debug_ (bool): A flag indicating whether to enable debugging mode.
        f (Callable[[float], float]): The function to find the root of.
        start_point (float): The starting point for the iteration.
        epsilon (float): The desired accuracy for the root finding.
        h (float, optional): The step size for the iteration. Defaults to 0.000001.

    Returns:
        RootFindingData: An object containing the root value,
            iteration points, and the number of iterations.

    """
    points: list[tuple[float, float]] = []
    current_point = start_point
    for i in range(MAX_ITER):
        value = f(current_point)
        if abs(value) < epsilon:
            return RootFindingData(
                value=current_point, iteration_points=points, iteration_no=i
            )
        if debug_:
            points.append((current_point, value))
        value_h = f(current_point + h)
        next_point = current_point + h * (1 - value_h / (value_h - value))
        current_point = next_point
    return RootFindingData(value=None, iteration_points=points, iteration_no=i)


@debug()
def root_secant(
    debug_: bool,
    f: Callable[[float], float],
    point_zero: float,
    point_one: float,
    epsilon: float,
) -> RootFindingData:
    """
    Finds the root of a function using the secant method.

    Args:
        debug_ (bool): A flag indicating whether to enable debug mode.
        f (Callable[[float], float]): The function to find the root of.
        point_zero (float): The initial guess for the root.
        point_one (float): The second initial guess for the root.
        epsilon (float): The desired accuracy for the root.

    Returns:
        RootFindingData: An object containing the root value,
            iteration points, and the number of iterations.

    """
    points: list[tuple[float, float]] = []
    for i in range(MAX_ITER):
        value_zero = f(point_zero)
        value_one = f(point_one)
        if abs(value_one) < epsilon:
            return RootFindingData(
                value=point_one, iteration_points=points, iteration_no=i
            )
        if debug_:
            points.append((point_zero, value_zero))
        point_next = point_one - value_one * (point_one - point_zero) / (
            value_one - value_zero
        )
        point_zero, point_one = point_one, point_next
    return RootFindingData(value=None, iteration_points=points, iteration_no=i)


@debug()
def root_bisection(
    debug_: bool,
    f: Callable[[float], float],
    a: float,
    b: float,
    epsilon: float,
    weighted: bool,
) -> RootFindingData:
    """
    Finds the root of a function using the bisection method.

    Args:
        debug_ (bool): A flag indicating whether to enable debug mode.
        f (Callable[[float], float]): The function to find the root of.
        a (float): The lower bound of the search interval.
        b (float): The upper bound of the search interval.
        epsilon (float): The desired accuracy of the root finding process.
        weighted (bool): A flag indicating whether to use weighted midpoint calculation.

    Returns:
        RootFindingData: An object containing the root value,
            iteration points, and the number of iterations.

    Raises:
        Exception: If the sign of the function values at the endpoints are the same.

    """
    points: list[tuple[float, float]] = []
    y_1: float = f(a)
    y_2: float = f(b)
    check: float = y_1 * y_2

    if check == 0:
        return RootFindingData(
            value=(a if y_1 == 0 else b),
            iteration_points=[],
            iteration_no=0,
        )
    if check > 0:
        raise ValueError("Root finding failed. f(a) and f(b) have the same sign")

    for i in range(MAX_ITER):
        i += 1
        y_1, y_2 = f(a), f(b)
        midpoint: float = (
            (-a * y_2 + b * y_1) / (y_1 - y_2) if weighted else (a + b) / 2
        )
        y_3: float = f(midpoint)
        if debug_:
            points.append((midpoint, y_3))
        if abs(y_3) < epsilon:
            return RootFindingData(
                value=midpoint,
                iteration_points=points,
                iteration_no=i,
            )
        if y_1 * y_3 < 0:
            b = midpoint
        else:
            a = midpoint
    return RootFindingData(value=None, iteration_points=points, iteration_no=i)


if __name__ == "__main__":

    def test_function(x: float) -> float:
        return x**3 - sin(x)

    EPSILON: Final[float] = 1e-12
    ANIMATED: Final[bool] = True

    result1 = root_newton(test_function, 1, EPSILON)
    result2 = root_secant(test_function, 0.1, 1, EPSILON)
    result3 = root_bisection(test_function, 0.1, 1, EPSILON, weighted=False)
    result4 = root_bisection(test_function, 0.1, 1, EPSILON, weighted=True)

    if ANIMATED:
        results = [
            (result1, "newton"),
            (result2, "secant"),
            (result3, "bisection"),
            (result4, "bisection weighted"),
        ]
        for result, name in results:
            print(f"result {name}: {result}")
            animate_data(result.iteration_points)
