numbers = [2, 5, 8, 12, 17, 21, 27, 31, 40]
target = 27

def binary_search(numbers, target):
    left = 0
    right = len(numbers)-1

    while left <= right:
        middle = (left + right) // 2

        if numbers[middle] == target:
            return f"The target is at index {middle}"
        elif numbers[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
    return "Target is not in list"

result = binary_search(numbers, 27)
print(result)