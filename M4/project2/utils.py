# Utility functions for Binary Search Tree

# Simple utility functions

import random

def generate_random_integers(count, max_value, seed=None):
    # generate unique random integers
    if seed:
        random.seed(seed)
    
    numbers = []
    while len(numbers) < count:
        num = random.randint(1, max_value)
        if num not in numbers:
            numbers.append(num)
    return numbers

def print_separator():
    # print a line separator
    print("-" * 50)

def format_list_preview(lst, max_items=10):
    # format list for display
    if len(lst) <= max_items:
        return str(lst)
    else:
        return str(lst[:max_items]) + "..."
