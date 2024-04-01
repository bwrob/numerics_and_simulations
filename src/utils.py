"""Common utility functions and decorators."""

import time
from typing import Any, Callable, NamedTuple, Union


def debug(control: str = "yny") -> Callable[[Callable], Callable]:
    """
    Decorator function that adds debugging capabilities to other functions.

    Parameters:
        control (str): A string specifying the control options for debugging.
            The string should have three characters, representing the debug, value, and timer options.
            The debug option can be 'y' or 'n', indicating whether to enable or disable debugging.
            The value option can be 'y' or 'n', indicating whether to print the result value.
            The timer option can be 'y' or 'n', indicating whether to print the execution time.

    Returns:
        function: Decorated function with debugging capabilities.

    """
    debug_, value, timer = control

    def wrapper(func: Callable) -> Callable:
        def wrapped(*args: Any, **kwargs: Any) -> Union[NamedTuple, Any]:
            if timer == "y":
                start = time.perf_counter()
            result = func(bool(debug_ == "y"), *args, **kwargs)
            if timer == "y":
                end = time.perf_counter()
                print(f"{func.__name__} evaluated in {end - start:.4f} seconds")

            if value == "y":
                try:
                    return result.value
                except AttributeError:
                    pass
            return result

        return wrapped

    return wrapper
