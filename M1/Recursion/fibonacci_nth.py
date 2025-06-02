def nth_fib(num):
    # Base case: the first two Fibonacci numbers are 0 and 1
    if num <= 2:
        return num - 1
    # Recursive case: sum of the two preceding Fibonacci numbers
    return nth_fib(num - 1) + nth_fib(num - 2)

# Test Cases
print(nth_fib(10)) #Output: 34

print(nth_fib(5)) #Output: 3

print(nth_fib(3)) #Output: 1