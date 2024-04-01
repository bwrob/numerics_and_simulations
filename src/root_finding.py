from math import sin

from utils import RootFindingData, animate, debugging


# Newton Method
# We are considering only single multiplicity isolated real roots
# 1. Find a starting point x_0 "close" to the root
# 2. Iterate x_{n+1} = x_n - f(x_n)/f'(x_n)
# 3. x^* = Lim x_n
@debugging()
def root_newton(debug, f, start_point, epsilon, h=0.000001):
    max_iter = 100000
    i = 0
    points = []
    current_point = start_point
    while i < max_iter:
        i += 1
        value = f(current_point)
        if abs(value) < epsilon:
            return RootFindingData(
                value=current_point, iteration_points=points, iteration_no=i
            )
        if debug:
            points.append((current_point, value))
        value_h = f(current_point + h)
        next_point = current_point + h * (1 - value_h / (value_h - value))
        current_point = next_point
    return RootFindingData(value=None, iteration_points=points, iteration_no=i)


# Secant Method
# We are considering only single multiplicity isolated real roots
# 1. Find two starting points x_0,x_1 "close" to the root
# 2. Iterate x_{n+1} = x_n - f(x_n)*(f(x_n) - f(x{n-1}))/(x_n - x_{n-1})
# 3. x^* = Lim x_n
@debugging()
def root_secant(debug, f, point_zero, point_one, epsilon):
    max_iter = 100000
    i = 0
    points = []
    while i < max_iter:
        i += 1
        value_zero = f(point_zero)
        value_one = f(point_one)
        if abs(value_one) < epsilon:
            return RootFindingData(
                value=point_one, iteration_points=points, iteration_no=i
            )
        if debug:
            points.append((point_zero, value_zero))
        point_next = point_one - value_one * (point_one - point_zero) / (
            value_one - value_zero
        )
        point_zero, point_one = point_one, point_next
    return RootFindingData(value=None, iteration_points=points, iteration_no=i)


# Bisection Method
# We are considering only single multiplicity isolated real roots
# 1. Find a suspect interval (a,b) for which f(a)*f(b)<0
# 2. Compute midpoint.
#   a) if unweighted then simple average
#   b) if weighted then find root of linear interpolation (a,f(a)) and (b,f(b))
# 3. Choose (a,midpoint) or (midpoint,b) depending on condition 1. Iterate.
# 4. x^* = lim of midpoints
@debugging()
def root_bisection(debug, f, a, b, epsilon, weighted):
    i = 0
    points = []
    max_iter = 10000
    y_1, y_2 = f(a), f(b)
    check = y_1 * y_2
    if check == 0:
        return a if y_1 == 0 else b
    if check > 0:
        raise Exception("nope")
    while i < max_iter:
        i += 1
        y_1, y_2 = f(a), f(b)
        midpoint = (-a * y_2 + b * y_1) / (y_1 - y_2) if weighted else (a + b) / 2
        y_3 = f(midpoint)
        if debug:
            points.append((midpoint, y_3))
        if abs(y_3) < epsilon:
            return RootFindingData(
                value=midpoint, iteration_points=points, iteration_no=i
            )
        if y_1 * y_3 < 0:
            a, b = a, midpoint
        else:
            a, b = midpoint, b
    return RootFindingData(value=None, iteration_points=points, iteration_no=i)


if __name__ == "__main__":
    f = lambda x: x**3 - sin(x)
    g = lambda x: (x + 2) * (x - 0.5) + sin(x - 0.5)
    func = f
    accuracy = 1e-12
    animated = False

    result1 = root_newton(func, 1, accuracy)
    print("result Newton: {}".format(result1))
    if animated:
        animate(result1.iteration_points)

    result2 = root_secant(func, 0.1, 1, accuracy)
    print("result secant: {}".format(result2))
    if animated:
        animate(result2.iteration_points)

    result3 = root_bisection(func, 0.1, 1, accuracy, weighted=False)
    print("result bisection: {}".format(result3))
    if animated:
        animate(result3.iteration_points)
    result4 = root_bisection(func, 0.1, 1, accuracy, weighted=True)
    print("result bisection: {}".format(result4))
    if animated:
        animate(result4.iteration_points)
