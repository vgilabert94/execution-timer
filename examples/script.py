"""Example file."""

from execution_timer import ExecutionTimer

et = ExecutionTimer(save_measure=True, n_iter=5)


# Example usage
@et.time_execution(return_measure=True, print_measure=True)
def multiply(n):
    return sum([i * j for i in range(1, n, 1) for j in range(n, 1, -1)])


# Running the example function multiple times
n = 2500
res = multiply(n)

times_result = et.get_measured_time()
print(times_result)
avg_result = et.average_measured_time()
print(avg_result)
