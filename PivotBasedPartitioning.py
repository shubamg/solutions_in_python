def f(input, pivot):
    right = len(input) - 1
    left = 0
    mid = 0
    print(list(enumerate(input)), "({:d}, {:d}, {:d})".format(left, mid, right))
    while mid <= right:
        if input[mid] > pivot:
            input[right], input[mid] = input[mid], input[right]
            right -= 1
        elif input[mid] == pivot:
            mid += 1
        else:
            input[left], input[mid] = input[mid], input[left]
            left += 1
            mid += 1
        print(list(enumerate(input)), "({:d}, {:d}, {:d})".format(left, mid, right))


f([1, 78, 3, -50, 4, 78, 6, 345, 67, 9, -900, 78, 945, 600], 78)
