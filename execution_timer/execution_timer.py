from __future__ import annotations

import warnings
from functools import wraps
from inspect import ismethod
from time import perf_counter, perf_counter_ns
from typing import Any, Callable, Optional, Union


def CHECK_CONDITION(
    condition: bool,
    name_var: str,
    msg: Optional[str] = None,
    default: Any = None,
    raise_exception: bool = False,
) -> Any:
    """
    Check a condition and handle the result accordingly.

    Parameters:
    -----------
    condition : bool
        The condition to check.
    name_var : str
        The name of the variable associated with the condition.
    msg : str, optional
        An optional message to include in the warning or exception.
    default : Any, optional
        The default value to return if the condition is False and no exception is raised.
    raise_exception : bool, optional
        Whether to raise an exception if the condition is False (default is False).

    Returns:
    --------
    Any
        Returns True if the condition is True. If the condition is False, it either raises an exception,
        returns the default value (if provided), or returns False.

    Raises:
    -------
    Exception
        If raise_exception is True and the condition is False, an exception is raised with the given message.

    """

    if condition:
        return True

    message = f"Condition not true.\n{msg}"

    if raise_exception:
        raise Exception(message)

    warnings.warn(
        f"{message}",
        UserWarning,
    )
    return False


def CHECK_TYPE(
    var: Any,
    name_var: str,
    expected: Union[type, tuple[type, ...]],
    default: Any = None,
    raise_exception: bool = False,
) -> Any:
    """
    Check the type of a variable and either return the variable or a default value.

    Parameters:
    -----------
    var : Any
        The variable to check.
    name_var : str
        The name_var of the variable (for use in the warning or exception message).
    expected : Union[type, Tuple[type, ...]]
        The type or tuple of types that `var` is expected to be.
    default : Any
        The default value to return if `var` is not of type `expected`.
    raise_exception : bool, optional
        Whether to raise a TypeError instead of issuing a warning (default is False).

    Returns:
    --------
    Any
        `var` if it is of type `expected`, otherwise `default`.

    Raises:
    -------
    TypeError
        If `raise_exception` is True and `var` is not of type `expected`.
    """

    if not isinstance(var, expected):
        message = f"Expected type of `{name_var}` is {expected.__name__}, but got '{type(var).__name__}'."
        if raise_exception:
            raise TypeError(f"{message}")
        else:
            warnings.warn(
                f"{message} Execution continues with default value ({name_var}={default}).",
                UserWarning,
            )
        return default

    return var


def time_execution(
    func: Callable[..., Any] = None,
    *,
    return_measure: bool = False,
    nanoseconds: bool = False,
    n_iter: int = 1,
    return_average: bool = True,
) -> Union[Callable[..., Any], Any]:
    """
    Decorator to measure the execution time of a function or method over multiple iterations.

    Parameters:
    -----------
    return_measure : bool, optional
        Whether to return the measured time along with the function result (default is False).
    nanoseconds : bool, optional
        Whether to use nanoseconds resolution for timing measurements (default is False).
    n_iter : int, optional
        The number of iterations to execute the function/method (default is 1).
        If n_iter > 1 and return_measure=True: result of the function will be the last execution.
    return_average : bool, optional
        Whether to return the average time when measuring over multiple iterations (default is True).
        Only is used when n_iter > 1.

    Returns:
    --------
    wrapper : callable
        Decorated function that measures the execution time of `func`.

    Notes:
    ------
    - If return_measure=False and return_average=False: a message will be printed for each iteration.
    - If n_iter > 1 and return_measure=True: the result will be the last function result.
    - If n_iter > 1 and return_measure=True and return_average=False: the result will be the last function result with a list of times for each iteration.
    """

    return_measure = CHECK_TYPE(return_measure, "return_measure", bool, False)
    nanoseconds = CHECK_TYPE(nanoseconds, "nanoseconds", bool, False)
    n_iter = CHECK_TYPE(n_iter, "n_iter", int, 1)
    n_iter = (
        n_iter
        if CHECK_CONDITION(
            n_iter >= 1,
            "n_iter",
            "Value of `n_iter` must be >= 1.",
        )
        else 1
    )
    return_average = CHECK_TYPE(return_average, "return_average", bool, True)

    # Define timer in seconds or nanoseconds.
    counter = perf_counter_ns if nanoseconds else perf_counter

    def decorator(inner_func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(inner_func)
        def wrapper(*args: tuple, **kwargs: dict) -> Union[Any, tuple[Any, float]]:
            elapsed_times = []
            for i in range(n_iter):
                start_time = counter()
                try:
                    result = inner_func(*args, **kwargs)
                except Exception as e:
                    raise e
                end_time = counter()
                elapsed_time = end_time - start_time
                elapsed_times.append(elapsed_time)

                if not return_measure and not return_average:
                    print(
                        f"Iteration {i+1}/{n_iter}. The '{inner_func.__name__}' function was executed in {elapsed_time:.5f} {'nanoseconds' if nanoseconds else 'seconds'}."
                    )

            if return_measure:
                if n_iter > 1:
                    if return_average:
                        return result, sum(elapsed_times) / n_iter
                    else:
                        return result, elapsed_times
                else:
                    return result, elapsed_times[0]
            else:
                if n_iter > 1:
                    if return_average:
                        print(
                            f"Iterations: {n_iter}. The '{inner_func.__name__}' function was executed in an average of {sum(elapsed_times) / n_iter:.5f} {'nanoseconds' if nanoseconds else 'seconds'} per iteration."
                        )
                else:
                    print(
                        f"The '{inner_func.__name__}' function was executed in {elapsed_times[0]:.5f} {'nanoseconds' if nanoseconds else 'seconds'}."
                    )
                return result

        return wrapper

    if func is None:
        return decorator

    return decorator(func)


class ExecutionTimer:
    """
    A utility class for measuring execution times of functions or methods.

    Parameters:
    -----------
    save_measure : bool, optional
        Flag to determine if measurement results should be saved (default is True).
    return_measure : bool, optional
            Flag to indicate if the measured time should be returned along with the function result.
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
    return_measure : bool
        Flag to indicate if the measured time should be returned along with the function result.
        If is False, will be print the execution time.

    Notes:
    ------
    - If n_iter > 1 and return_measure=True: the result will be the last function result.
    - If n_iter > 1 and return_measure=False: the time printed will be the last execution result.

    """

    def __init__(
        self,
        save_measure: bool = True,
        return_measure: bool = False,
        nanoseconds: bool = False,
        n_iter: int = 1,
    ) -> None:
        """
        Initialize an ExecutionTimer instance.
        """

        save_measure = CHECK_TYPE(save_measure, "save_measure", bool, True)
        return_measure = CHECK_TYPE(return_measure, "return_measure", bool, False)
        nanoseconds = CHECK_TYPE(nanoseconds, "nanoseconds", bool, False)
        n_iter = CHECK_TYPE(n_iter, "n_iter", int, 1)
        n_iter = (
            n_iter
            if CHECK_CONDITION(
                n_iter >= 1,
                "n_iter",
                "Value of `n_iter` must be >= 1.",
            )
            else 1
        )

        self.execution_times: dict[str, list[float]] = {}
        self.save_measure: bool = save_measure
        self.nanoseconds: bool = nanoseconds
        self.counter = perf_counter_ns if self.nanoseconds else perf_counter
        self.n_iter = n_iter
        self.return_measure = return_measure

    def time_execution(
        self,
        func: Callable[..., Any] = None,
        *,
        return_measure: Optional[bool] = None,
    ) -> Union[Callable[..., Any], Any]:
        """
        Decorator method to measure the execution time of a function or method.

        Parameters:
        -----------
        func : callable, optional
            Function or method to be timed. If None, returns a decorator function.
        return_measure : bool, optional
            Flag to indicate if the measured time should be returned along with the function result.
            If not provided, the behavior defaults to the value set during class initialization.

        Returns:
        --------
        wrapper : callable
            Decorated function that measures the execution time of `func`.
        """

        return_measure = (
            self.return_measure
            if return_measure is None
            else CHECK_TYPE(return_measure, "return_measure", bool, False)
        )

        def decorator(inner_func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(inner_func)
            def wrapper(*args: tuple, **kwargs: dict) -> Union[Any, tuple[Any, float]]:
                for _ in range(self.n_iter):
                    start_time = self.counter()
                    try:
                        result = inner_func(*args, **kwargs)
                    except Exception as e:
                        raise e
                    end_time = self.counter()
                    elapsed_time = end_time - start_time

                    if self.save_measure:
                        func_name = inner_func.__name__
                        is_method = False
                        if len(args) > 0 and ismethod(
                            getattr(args[0], inner_func.__name__, None)
                        ):
                            class_name = args[0].__class__.__name__
                            is_method = True
                        if is_method:
                            if class_name not in self.execution_times:
                                self.execution_times[class_name] = {}
                            if func_name not in self.execution_times[class_name]:
                                self.execution_times[class_name][func_name] = []
                            self.execution_times[class_name][func_name].append(
                                elapsed_time
                            )
                        else:
                            if func_name not in self.execution_times:
                                self.execution_times[func_name] = []
                            self.execution_times[func_name].append(elapsed_time)

                if return_measure:
                    return result, elapsed_time
                else:
                    print(
                        f"The '{inner_func.__name__}' function was executed in {elapsed_time:.5f} {'nanoseconds' if self.nanoseconds else 'seconds'}."
                    )
                    return result

            return wrapper

        if func is None:
            return decorator

        return decorator(func)

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
