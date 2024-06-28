
# ExecutionTimer

ExecutionTimer is a utility class for measuring execution times of functions or methods in Python. It provides a **decorator** to easily measure and optionally save the execution times.

## Installation

- Install via pip:

```bash
pip install execution-timer
```

- Install via git clone:
```bash
git clone https://github.com/vgilabert94/execution-timer
```


## Documentation

### Class: `ExecutionTimer`

#### Parameters

- `save_measure` (bool, optional): Flag to determine if measurement results should be saved (default is True).
- `nanoseconds` (bool, optional): Flag to use nanoseconds resolution for timing measurements (default is False).
- `n_iter` : (int, optional): Number of iterations to execute the function/method (default is 1).

### Methods

#### `time_execution(self, func: Callable[..., Any] = None, *, return_measure: bool = False) -> Union[Callable[..., Any], Any]`

Decorator method to measure the execution time of a function or method.

- `func` (callable, optional): Function or method to be timed. If None, returns a decorator function.
- `return_measure` (bool, optional): Flag to indicate if the measured time should be returned along with the function result.
- `print_measure` (bool, optional): Flag to indicate if the measured time should be printed.

Returns:
- `wrapper` (callable): Decorated function that measures the execution time of `func`.

#### `get_measured_time(self) -> dict[str, Optional[float]]`

Retrieve the recorded execution times.

Returns:
- `dict`: Dictionary containing the measured execution times. Keys are function or method names, and values are lists of measured times.


#### `reset_measured_timedef reset_measured_time(self) -> None:`
Reset the recorded execution times.

#### `average_measured_time(self) -> dict[str, Optional[float]]:`
Calculate the average execution times for all recorded functions or methods.

Returns:
- `dict`: A dictionary where keys are function or class names, and values are the average execution times in seconds. If no times are recorded, the value will be None.


## Examples

You can access a comprehensive examples notebook at the following link: [examples/notebook.ipynb](examples/notebook.ipynb)

Load packages: 
```python
import time
from execution_timer import ExecutionTimer
```

### Example 1: Measuring a function with the default settings.

```python
timer = ExecutionTimer()

@timer.time_execution
def sample_function(n):
    time.sleep(n)

print(sample_function(n=2))
print(timer.get_measured_time())
```
Output
```bash
None
{'sample_function': [2.0000783540003795]}
```

### Example 4: Measuring N iterations

```python
timer = ExecutionTimer(n_iter=5)

@timer.time_execution()
def sample_function(n):
    time.sleep(n)

print(sample_function(n=1))
print(timer.get_measured_time())
print(timer.average_measured_time())
```
Output
```bash
None
{'sample_function': [1.0000926779994188, 1.0000929059988266, 1.00007422499948, 1.0001207340010296, 1.000119641999845]}
{'sample_function': 1.00010003699972}
```

### Example 6: Measuring a Method from a class

```python
timer = ExecutionTimer()

class SampleClass:
    def __init__(self):
        pass

    @timer.time_execution(return_measure=True)
    def sample_method(self, n):
        time.sleep(n)

    @timer.time_execution
    def sample_method_x2(self, n):
        time.sleep(2*n)

sample = SampleClass()
print(sample.sample_method(n=2))
print(sample.sample_method_x2(n=2))
print(timer.get_measured_time())
```
Output
```bash
(None, 2.0000849130010465)
None
{'SampleClass': {'sample_method': [2.0000849130010465], 'sample_method_x2': [4.000076272001024]}}
```

## LICENSE 

Distributed under the MIT License. See LICENSE.txt for more information.


## Contact

[Vicent Gilabert](mailto:gilabert_vicent@hotmail.com)

[Linkedin](https://www.linkedin.com/in/vgilabert/)
