
# ExecutionTimer

ExecutionTimer is a utility class for measuring execution times of functions or methods in Python. It provides a **decorator** to easily measure and optionally save the execution times.

## Installation

- Install via pip:

```bash
pip install timer-decorator
```

- Install via git clone:
```bash
git clone https://github.com/vgilabert94/execution-timer
```


## Documentation

### Function: `time_execution`

#### Parameters
- `return_measure` (bool, optional): Whether to return the measured time along with the function result (default is False).
- `nanoseconds` (bool, optional): Whether to use nanoseconds resolution for timing measurements (default is False).
- `n_iter` (int, optional): The number of iterations to execute the function/method (default is 1). If n_iter > 1 and return_measure=True: result of the function will be the last execution.
- `return_average` (bool, optional): Whether to return the average time when measuring over multiple iterations (default is True). Only is used when n_iter > 1.

#### Notes
- If `return_measure`=False and `return_average`=False: a message will be printed for each iteration.
- If `n_iter` > 1 and `return_measure`=True: the result will be the last function result.
- If `n_iter` > 1 and `return_measure`=True and `return_average`=False: the result will be the last function result with a list of times for each iteration.


### Class: `ExecutionTimer`

#### Parameters

- `save_measure` (bool, optional): Flag to determine if measurement results should be saved (default is True).
- `nanoseconds` (bool, optional): Flag to use nanoseconds resolution for timing measurements (default is False).
- `n_iter` : (int, optional): Number of iterations to execute the function/method (default is 1).

#### Notes
- If `n_iter` > 1 and `return_measure`=True: the result will be the last function result.
- If `n_iter` > 1 and `return_measure`=False: the time printed will be the last execution result.


#### Methods

#### `time_execution`

Decorator method to measure the execution time of a function or method.

- `func` (callable, optional): Function or method to be timed. If None, returns a decorator function.
- `return_measure` (bool, optional): Flag to indicate if the measured time should be returned along with the function result.
- `print_measure` (bool, optional): Flag to indicate if the measured time should be printed.

Returns:
- `wrapper` (callable): Decorated function that measures the execution time of `func`.

#### `get_measured_time`

Retrieve the recorded execution times.

Returns:
- `dict`: Dictionary containing the measured execution times. Keys are function or method names, and values are lists of measured times.


#### `reset_measured_time`
Reset the recorded execution times.

#### `average_measured_time`
Calculate the average execution times for all recorded functions or methods.

Returns:
- `dict`: A dictionary where keys are function or class names, and values are the average execution times in seconds. If no times are recorded, the value will be None.


## Examples

You can access a comprehensive examples notebook at the following link: [examples/notebook.ipynb](examples/notebook.ipynb)

Load packages: 
```python
import time
from execution_timer import ExecutionTimer, time_execution
```

### Example 1: Measuring a function with the default settings.

```python
timer = ExecutionTimer()

@timer.time_execution
def sample_function(n):
    time.sleep(n)

print(sample_function(n=1))
print(timer.get_measured_time())
```
Output
```bash
None
{'sample_function': [1.0000783540003795]}
```

```python
@time_execution
def sample_function(n):
    time.sleep(n)

print(sample_function(n=1))
```
Output
```bash
The 'sample_function' function was executed in 1.00085 seconds.
None
```

### Example 2: Measuring N iterations

```python
timer = ExecutionTimer(n_iter=5)

@timer.time_execution
def sample_function(n):
    time.sleep(n)

print(sample_function(n=1))
print(timer.get_measured_time())
print(timer.average_measured_time())
```
Output
```bash
The 'sample_function' function was executed in 1.00098 seconds.
None
{'sample_function': [1.0010039510007118, 1.001013477000015, 1.001078371999938, 1.0008607439995103, 1.0009819289998632]}
{'sample_function': 1.0009876946000076}
```

```python
@time_execution(n_iter=5)
def sample_function(n):
    time.sleep(n)

print(sample_function(n=1))
```
Output
```bash
The 'sample_function' function was executed in 1.00030 seconds.
None
```

### Example 8: Measuring a Method from a class

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
print(sample.sample_method(n=1))
print(sample.sample_method_x2(n=1))
print(timer.get_measured_time())
```
Output
```bash
(None, 1.0002362490004089)
The 'sample_method_x2' function was executed in 2.00203 seconds.
None
{'SampleClass': {'sample_method': [1.0002362490004089], 'sample_method_x2': [2.0020319710001786]}}
```

## LICENSE 

Distributed under the MIT License. See LICENSE.txt for more information.


## Contact

[Vicent Gilabert](mailto:gilabert_vicent@hotmail.com)

[Linkedin](https://www.linkedin.com/in/vgilabert/)
