def reverse(high, low, string_li):
    # Base case: when the pointers cross, the string is fully reversed
    if high <= low:
        return string_li
    else:
        # Swap the characters at positions high and low
        temp = string_li[high]
        string_li[high] = string_li[low]
        string_li[low] = temp
        # Recursive call, moving the pointers towards the center
        return reverse(high - 1, low + 1, string_li)
    
# Test Case
a = "Hello World"
# Convert string to list, reverse it, then join back to string
print(''.join(reverse(len(a) - 1, 0, list(a))))