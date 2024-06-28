from __future__ import annotations

import warnings
from functools import wraps
from inspect import ismethod
from time import perf_counter, perf_counter_ns
from typing import Any, Callable, Optional, Union


class ExecutionTimer:
    """
    A utility class for measuring execution times of functions or methods.

    Parameters:
    -----------
    save_measure : bool, optional
        Flag to determine if measurement results should be saved (default is True).
    nanoseconds : bool, optional
        Flag to use nanoseconds resolution for timing measurements (default is False).
    n_iter : int, optional
        Number of iterations to execute the function/method (default is 1).

    Attributes:
    ----------
    execution_times : dict
        Dictionary to store measured execution times. Keys are function or method names,
        and values are lists of measured times.
    save_measure : bool, optional
        Flag to control whether to save measured times (default is True).
    counter : callable
        Function used for timing measurements, either `time.perf_counter` or `time.perf_counter_ns`
        based on the `nanoseconds` flag provided during initialization.
    n_iter : int
        Number of iterations to execute the function/method.

    """

    def __init__(self, save_measure: bool = True, nanoseconds: bool = False, n_iter: int = 1) -> None:
        """
        Initialize an ExecutionTimer instance.
        """
        if not isinstance(save_measure, bool):
            save_measure = True
            warnings.warn(
                f"Expected type 'bool', but got '{type(save_measure).__name__}'. Execution continues with default value (save_measure=True).",
                UserWarning,
            )

        if not isinstance(nanoseconds, bool):
            nanoseconds = False
            warnings.warn(
                f"Expected type 'bool', but got '{type(nanoseconds).__name__}'. Execution continues with default value (nanoseconds=False).",
                UserWarning,
            )
        
        if not isinstance(n_iter, int) or n_iter <= 0:
            n_iter = 1
            warnings.warn(
                f"Expected a positive integer for 'n_iter', but got '{n_iter}'. Execution continues with default value (n_iter=1).",
                UserWarning,
            )

        self.execution_times: dict[str, list[float]] = {}
        self.save_measure: bool = save_measure
        self.nanoseconds: bool = nanoseconds
        self.counter = perf_counter_ns if self.nanoseconds else perf_counter
        self.n_iter = n_iter

    def time_execution(
        self,
        func: Callable[..., Any] = None,
        *,
        return_measure: bool = False,
        print_measure: bool = False,
    ) -> Union[Callable[..., Any], Any]:
        """
        Decorator method to measure the execution time of a function or method.

        Parameters:
        -----------
        func : callable, optional
            Function or method to be timed. If None, returns a decorator function.
        return_measure : bool, optional
            Flag to indicate if the measured time should be returned along with the function result.
        print_measure: bool, optional
            Flag to indicate if the measured time should be printed.
        
        Returns:
        --------
        wrapper : callable
            Decorated function that measures the execution time of `func`.
        """

        if not isinstance(return_measure, bool):
            return_measure = False
            warnings.warn(
                f"Expected type 'bool', but got '{type(return_measure).__name__}'. Execution continues with default value (return_measure=False).",
                UserWarning,
            )

        if not isinstance(print_measure, bool):
            print_measure = False
            warnings.warn(
                f"Expected type 'bool', but got '{type(print_measure).__name__}'. Execution continues with default value (print_result=False).",
                UserWarning,
            )

        if func is None:
            return lambda f: self.time_execution(
                f, return_measure=return_measure, print_measure=print_measure
            )

        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Union[Any, tuple[Any, float]]:
                
            for _ in range(self.n_iter):
                start_time = self.counter()
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    raise e
                end_time = self.counter()
                elapsed_time = end_time - start_time

                if print_measure:
                    print(
                        f"Function '{func.__name__}' executed in {elapsed_time:.5f} {'nanoseconds' if self.nanoseconds else 'seconds'}."
                    )

                if self.save_measure:
                    func_name = func.__name__
                    is_method = False
                    if len(args) > 0 and ismethod(getattr(args[0], func.__name__, None)):
                        class_name = args[0].__class__.__name__
                        is_method = True
                    if is_method:
                        if class_name not in self.execution_times:
                            self.execution_times[class_name] = {}
                        if func_name not in self.execution_times[class_name]:
                            self.execution_times[class_name][func_name] = []
                        self.execution_times[class_name][func_name].append(elapsed_time)
                    else:
                        if func_name not in self.execution_times:
                            self.execution_times[func_name] = []
                        self.execution_times[func_name].append(elapsed_time)

            if return_measure:
                return result, elapsed_time

            return result

        return wrapper

    def get_measured_time(self) -> dict[str, Optional[float]]:
        """
        Retrieve the recorded execution times.

        Returns:
        --------
        dict
            Dictionary containing the measured execution times. Keys are function or method names,
            and values are lists of measured times.
        """
        return self.execution_times

    def reset_measured_time(self) -> None:
        """
        Reset the recorded execution times.
        """
        self.execution_times.clear()

    def average_measured_time(self) -> dict[str, Optional[float]]:
        """
        Calculate the average execution times for all recorded functions or methods.

        Returns:
        --------
        dict[str, Optional[float]]:
            A dictionary where keys are function or class names, and values are the average
            execution times in seconds. If no times are recorded, the value will be None.
        """
        averages: dict[str, Optional[float]] = {}

        for key, value in self.execution_times.items():
            if isinstance(value, list):
                averages[key] = sum(value) / len(value) if value else None
            elif isinstance(value, dict):
                class_averages: dict[str, float] = {}
                for func_name, times in value.items():
                    class_averages[func_name] = (
                        sum(times) / len(times) if times else None
                    )
                averages[key] = class_averages

        return averages
