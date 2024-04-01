"""Common utility functions and decorators."""

import time
from typing import Any, Callable, NamedTuple, Union


def debugging(control: str = "yny") -> Callable[[Callable], Callable]:
    """
    Decorator function that adds debugging capabilities to other functions.

    Parameters:
        control (str): A string specifying the control options for debugging.
            The string should have three characters, representing the debug, value, and timer options.
            The debug option can be 'y' or 'n', indicating whether to enable or disable debugging.
            The value option can be 'y' or 'n', indicating whether to print the result value.
            The timer option can be 'y' or 'n', indicating whether to print the execution time.

    Returns:
        function: The decorated function with debugging capabilities.

    Example:
        @debugging("yny")
        def my_function(debug: bool, x: int) -> NamedTuple('Result', [('value', int)]):
            if debug:
                print("Debugging is enabled")
            return Result(value=x**2)

        result = my_function(True, 5)
        # Output: Debugging is enabled
        #         my_function evaluated in 0.0001 seconds
        #         25

    Note:
        The decorated function should accept a debug parameter as the first argument.
        The debug parameter is used to control the debugging behavior within the function.
        If the debug parameter is set to True, additional debugging information will be printed.
        If the value parameter is set to True, the result value will be printed.
        If the timer parameter is set to True, the execution time will be printed.

    """
    debug, value, timer = control

    def wrapper(f: Callable) -> Callable:
        def wrapped(*args: Any, **kwargs: Any) -> Union[NamedTuple, Any]:
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
