"""
Task 2 Testing - BST Operations and Function Testing
Purpose: Test basic BST operations with 64 random integers
Author: Van Robbins
"""


import time
from bst import BinarySearchTree
from utils import generate_random_integers


def test_bst_basic_operations():
    # Test BST operations with 64 random integers
    print("TASK 2: BST OPERATIONS AND FUNCTION TESTING")
    print("=" * 60)
    
    # Generate 64 unique random integers within range [1, 128]
    random_values = generate_random_integers(64, 128)
    print("Generated 64 random integers: " + str(random_values[:10]) + "..." + str(random_values[-10:]))
    
    # Create BST and insert all values
    bst = BinarySearchTree()
    print("Inserting all values into BST...")
    
    start_time = time.time()
    for value in random_values:
        bst.insert(value)
    insertion_time = time.time() - start_time
    
    print("All values inserted successfully!")
    print("Tree height after all insertions: " + str(bst.height()))
    print("Insertion time: " + str(round(insertion_time, 4)) + " seconds")
    
    # Search operations
    print("\nSEARCH OPERATIONS")
    print("-" * 40)
    
    search_values = [random_values[0], random_values[len(random_values)//2], random_values[-1]]
    search_labels = ["first", "middle", "last"]
    
    for value, label in zip(search_values, search_labels):
        start_time = time.time()
        found = bst.search(value)
        search_time = time.time() - start_time
        print("Search for " + str(value) + " (" + label + " value): " + ("Found" if found else "Not Found") + 
              " (Time: " + str(round(search_time, 6)) + "s)")
    
    # Test search for non-existent value
    non_existent = 999
    found = bst.search(non_existent)
    print("Search for " + str(non_existent) + " (non-existent): " + ("Found" if found else "Not Found"))
    
    # Traversal outputs
    print("\nTRAVERSAL OPERATIONS")
    print("-" * 40)
    
    in_order = bst.in_order_traversal()
    pre_order = bst.pre_order_traversal()
    post_order = bst.post_order_traversal()
    
    print("In-order traversal (first 20): " + str(in_order[:20]))
    print("Pre-order traversal (first 20): " + str(pre_order[:20]))
    print("Post-order traversal (first 20): " + str(post_order[:20]))
    
    # Verify in-order is sorted
    is_sorted = all(in_order[i] <= in_order[i+1] for i in range(len(in_order)-1))
    print("In-order traversal is sorted: " + str(is_sorted))
    
    # Deletion operations
    print("\nDELETION OPERATIONS")
    print("-" * 40)
    
    for value, label in zip(search_values, search_labels):
        print("Deleting " + str(value) + " (" + label + " value)...")
        bst.delete(value)
        height_after_deletion = bst.height()
        in_order_after = bst.in_order_traversal()
        print("Tree height after deletion: " + str(height_after_deletion))
        print("In-order traversal (first 15): " + str(in_order_after[:15]))
        print("Remaining nodes: " + str(len(in_order_after)))
        print()
    
    print("Final tree height: " + str(bst.height()))
    print("Final number of nodes: " + str(len(bst.in_order_traversal())))


def run_task2_tests():
    # wrapper function to run task 2 tests
    print("Starting Task 2: BST Operations and Function Testing")
    print("=" * 60)
    test_bst_basic_operations()
    print("Task 2 testing completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    run_task2_tests()
