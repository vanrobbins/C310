def binary_search(arr, target, offset=0):
    # Base case: if the array is empty, target is not found
    if(len(arr)==0):
        return -1;
    # Find the middle index int
    mid_Idx=len(arr)//2
    # If the middle element is the target, return its index (adjusted by offset)
    if(arr[mid_Idx]==target):
        return offset+mid_Idx;
    # If the middle element is less than the target, search the right half
    elif(arr[mid_Idx]<target):
        # Increase offset since we're skipping the left half including mid_Idx
        return binary_search(arr[mid_Idx+1:],target,offset+mid_Idx+1)
    else:
        # Otherwise, search the left half (offset remains the same)
        return binary_search(arr[:mid_Idx],target, offset)

# Test Cases
array_a = [1, 3, 5, 7, 9, 11, 13, 15] 
target_a = 7
print(binary_search(array_a,target_a))  # Output: 3

array_b = [2, 4, 6, 8, 10] 
target_b = 5 
print(binary_search(array_b,target_b))  # Output: -1

array_c = [4, 12, 18, 27, 34, 56, 67, 89]
target_c = 56
print(binary_search(array_c, target_c)) # Output: 5