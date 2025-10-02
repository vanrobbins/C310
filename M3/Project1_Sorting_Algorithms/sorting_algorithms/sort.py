"""
Sorting Algorithms Implementations
----------------------------------
Provides implementations of Bubble Sort, Insertion Sort, Merge Sort, Quick Sort, and Radix Sort.
All algorithms operate in-place unless otherwise noted.
Intended for benchmarking and educational purposes.
"""

# -- BUBBLE SORT --
def bubble_sort(arr):
    """
    In-place Bubble Sort.
    Sorts arr in ascending order.
    """
    for i in range(0, len(arr)-1):
        for j in range(0, len(arr)-1-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# -- INSERTION SORT --
def insertion_sort(arr):
    """
    In-place Insertion Sort.
    Sorts arr in ascending order.
    """
    for i in range(1, len(arr)):
        currNum = arr[i]
        j = i-1
        while j >= 0 and currNum < arr[j]:  # Move elements greater than key one position ahead
            arr[j+1] = arr[j]  # Shift elements to the right
            j -= 1
        arr[j+1] = currNum
    return arr

# -- QUICK SORT --
def quick_sort(arr):
    """
    In-place Quick Sort.
    Sorts arr in ascending order.
    """
    quick_sort2(arr, 0, len(arr) - 1)

def quick_sort2(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        quick_sort2(arr, low, p - 1)
        quick_sort2(arr, p + 1, high)

def get_pivot(arr, low, high):
    """
    Median-of-three pivot selection for Quick Sort.
    Returns pivot index.
    """
    mid = (low + high) // 2
    pivot = high
    if (arr[low] < arr[mid] < arr[high]) or (arr[high] < arr[mid] < arr[low]):
        pivot = mid
    elif (arr[mid] <= arr[low] <= arr[high]) or (arr[high] <= arr[low] <= arr[mid]):
        pivot = low
    return pivot

def partition(arr, low, high):
    """
    Partition function for Quick Sort.
    """
    pivotIndex = get_pivot(arr, low, high)
    pivotValue = arr[pivotIndex]
    arr[pivotIndex], arr[high] = arr[high], arr[pivotIndex]  # Move pivot to end
    storeIndex = low
    for i in range(low, high):
        if arr[i] < pivotValue:
            arr[i], arr[storeIndex] = arr[storeIndex], arr[i]
            storeIndex += 1
    arr[storeIndex], arr[high] = arr[high], arr[storeIndex]  # Move pivot to its final place
    return storeIndex

# -- MERGE SORT --
def merge_sort(arr):
    """
    Out-of-place Merge Sort.
    Returns a new sorted list.
    """
    if len(arr) < 2:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    """
    Merge helper for Merge Sort.
    Merges two sorted lists into one.
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# -- RADIX SORT --
def counting_sort(arr, exp):
    """
    Counting sort subroutine for Radix Sort.
    Sorts arr by the digit at exp (10^exp place).
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # Count occurrences
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    # Cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build output array
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    # Copy to arr
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    """
    In-place Radix Sort (LSD, base 10).
    Sorts arr in ascending order.
    """
    if len(arr) == 0:
        return
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
