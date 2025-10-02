"""
Main BST Project Runner
Author: Van Robbins
"""
import sys
import time

# Import task modules  
from task2_testing import run_task2_tests
from task3_testing import run_task3_tests

def print_project_header():
    # print the project header
    print("BINARY SEARCH TREE IMPLEMENTATION AND ANALYSIS")
    print("=" * 50)

def run_all_tasks():
    # run all project tasks in sequence
    print_project_header()
    print("RUNNING ALL TASKS")
    print("-" * 30)
    
    start_time = time.time()
    
    print("EXECUTING TASK 2...")
    run_task2_tests()
    print()
    
    print("EXECUTING TASK 3...")
    run_task3_tests()
    
    total_time = time.time() - start_time
    print()
    print("ALL TASKS COMPLETED")
    print("Total time:", round(total_time, 2), "seconds")

def run_demo_mode():
    # run a quick demonstration of BST capabilities
    print_project_header()
    print("DEMO MODE - Quick BST Demonstration")
    print("-" * 30)
    
    from bst import BinarySearchTree
    import random
    
    # create BST and add some numbers
    bst = BinarySearchTree()
    
    # generate some random numbers for demo
    random.seed(42)
    numbers = []
    while len(numbers) < 10:
        num = random.randint(1, 50)
        if num not in numbers:
            numbers.append(num)
    
    print("Inserting numbers:", numbers)
    for num in numbers:
        bst.insert(num)
    
    print("Tree height:", bst.height())
    print("In-order traversal:", bst.in_order_traversal())
    
    # test search
    search_val = numbers[0]
    print("Searching for", search_val, ":", bst.search(search_val))
    
    # test delete
    delete_val = numbers[0]
    bst.delete(delete_val)
    print("After deleting", delete_val, ":", bst.in_order_traversal())
    
    print("Demo completed!")

def main():
    # main entry point
    print("Choose what to run:")
    print("1. All tasks")
    print("2. Task 2 only") 
    print("3. Task 3 only")
    print("4. Demo")
    
    choice = input("Enter choice (1-4): ")
    
    if choice == "1":
        run_all_tasks()
    elif choice == "2":
        run_task2_tests()
    elif choice == "3":
        run_task3_tests()
    elif choice == "4":
        run_demo_mode()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
