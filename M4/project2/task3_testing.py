# Task 3 testing for BST with different data sets

import time
from bst import BinarySearchTree

def generate_random_integers(count, max_value):
    # generate random unique integers
    import random
    random.seed(42)  # for consistent results
    numbers = []
    while len(numbers) < count:
        num = random.randint(1, max_value)
        if num not in numbers:
            numbers.append(num)
    return numbers

def test_different_datasets():
    # test BST with different sized random datasets
    print("TASK 3: TESTING WITH DIFFERENT DATA SETS")
    print("=" * 50)
    
    datasets = [
        (256, 512, "256 integers from [1, 512]"),
        (128, 256, "128 integers from [1, 256]"),
        (64, 128, "64 integers from [1, 128]")
    ]
    
    results = []
    
    for count, max_val, description in datasets:
        print()
        print("TESTING:", description)
        print("-" * 40)
        
        # generate random data
        random_data = generate_random_integers(count, max_val)
        
        # create and populate BST
        bst = BinarySearchTree()
        start_time = time.time()
        
        for value in random_data:
            bst.insert(value)
        
        insertion_time = time.time() - start_time
        height = bst.height()
        in_order = bst.in_order_traversal()
        
        print("Inserted", count, "values")
        print("Tree height:", height)
        print("Insertion time:", round(insertion_time, 4), "seconds")
        print("In-order traversal (first 10):", in_order[:10])
        
        results.append({
            'description': description,
            'count': count,
            'height': height,
            'insertion_time': insertion_time
        })
    
    return results

def test_worst_case_scenarios():
    # test worst-case scenarios with ascending sequences
    print()
    print("WORST-CASE SCENARIO TESTING")
    print("=" * 40)
    
    worst_case_sizes = [64, 128, 256]
    worst_case_results = []
    
    for size in worst_case_sizes:
        print()
        print("WORST CASE: Ascending sequence [1, 2, 3, ...", str(size) + "]")
        print("-" * 40)
        
        # create ascending sequence
        ascending_data = list(range(1, size + 1))
        
        # create and populate BST
        bst = BinarySearchTree()
        start_time = time.time()
        
        for value in ascending_data:
            bst.insert(value)
        
        insertion_time = time.time() - start_time
        height = bst.height()
        
        print("Inserted", size, "values in ascending order")
        print("Tree height:", height, "(worst-case: like a linked list)")
        print("Expected height for balanced tree: about", size.bit_length())
        print("Insertion time:", round(insertion_time, 4), "seconds")
        
        worst_case_results.append({
            'size': size,
            'height': height,
            'insertion_time': insertion_time
        })
    
    return worst_case_results

def run_task3_tests():
    # main function to run all task 3 tests
    random_results = test_different_datasets()
    worst_case_results = test_worst_case_scenarios()
    
    print()
    print("TASK 3 COMPLETED")
    print("=" * 30)
    
    return random_results, worst_case_results

if __name__ == "__main__":
    run_task3_tests()
