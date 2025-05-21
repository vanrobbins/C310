def nth_fib(num):
    # Base case: the first two Fibonacci numbers are 0 and 1
    if num <= 2:
        return num - 1
    # Recursive case: sum of the two preceding Fibonacci numbers
    return nth_fib(num - 1) + nth_fib(num - 2)

# Test Case: Print the 10th Fibonacci number
print(nth_fib(10))