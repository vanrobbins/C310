def reverse(high, low, string_li):
    # Convert input to list if it's a string (for mutability)
    if type(string_li) == str:
        string_li = list(string_li)
    # Base case: when the pointers cross or meet, the string is fully reversed
    if high <= low:
        return ''.join(string_li)
    else:
        # Swap the characters at positions high and low
        temp = string_li[high]
        string_li[high] = string_li[low]
        string_li[low] = temp
        # Recursive call, moving the pointers towards the center
        return reverse(high - 1, low + 1, string_li)

# Test Cases
a = "Hello World"
print(reverse(len(a) - 1, 0, a))  #Output: dlroW olleH

b = "Indiana University"
print(reverse(len(b) - 1, 0, b)) #Output: ytisrevinU anaidnI

c = "Racecar"
print(reverse(len(c) - 1, 0, c)) #Output: racecaR