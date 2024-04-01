"""Common utility functions and decorators."""

import time
from typing import Any, Callable, NamedTuple, Union


def debug(debug_control: str = "yny") -> Callable[[Callable], Callable]:
    """
    A decorator that enables debugging features based on the debug_control string.

    Parameters:
        debug_control (str): A string indicating which debugging features to enable
            (e.g., 'yyy' enables all features).

    Returns:
        Callable[[Callable], Callable]: A decorator function that can be used to
            enable debugging features for another function.

    """
    debug_enabled, value_print, timer_print = debug_control

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Union[NamedTuple, Any]:
            if timer_print == "y":
                start = time.perf_counter()

            result = func(bool(debug_enabled == "y"), *args, **kwargs)

            if timer_print == "y":
                end = time.perf_counter()
                execution_time = end - start
                func_name = func.__name__
                print(f"{func_name} evaluated in {execution_time:.4f} seconds")

            if value_print == "y":
                try:
                    return result.value
                except AttributeError:
                    pass

            return result

        return wrapper

    return decorator
