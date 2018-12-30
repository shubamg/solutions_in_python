"""This problem was asked by Stripe.
Given an array of integers, find the first missing positive integer in linear time and constant space. In other words, find the lowest positive integer that does not exist in the array. The array can contain duplicates and negative numbers as well.
For example, the input [3, 4, -1, 1] should give 2. The input [1, 2, 0] should give 3.
You can modify the input array in-place."""
from __future__ import print_function


def get_mex_impurely(list_of_numbers):
    N = len(list_of_numbers)
    # Note that only members b/w 1 to n can affect the answer
    # All other numbers are noise. So make others zero
    # So the idea is to modify the input array arr, such that
    # arr[i] = -freq of i+1 in original array if arr[i] b/w 0 and -N

    def f(n):
        if n <= 0 or n > N:
            return 0 # -INF
        else:
            return n

    def is_important_value(x):
        # print "is_important_value", x, " is ", N >= x > 0
        return N >= x > 0

    list_of_numbers = [f(n) for n in list_of_numbers]
    print(list_of_numbers)
    index = 0
    while index < N:
        value_at_current_index = list_of_numbers[index]
        while is_important_value(value_at_current_index):
            frequency_index = value_at_current_index - 1
            value_at_frequency_index = list_of_numbers[frequency_index]

            # print(index, "-> ", value_at_current_index, frequency_index, "-> ", value_at_frequency_index)

            if is_important_value(value_at_frequency_index):
                list_of_numbers[frequency_index] = -1
                if frequency_index != index:
                    list_of_numbers[index] = value_at_frequency_index
            else:
                list_of_numbers[frequency_index], list_of_numbers[index] = value_at_frequency_index-1, 0

            value_at_current_index = list_of_numbers[index]

        #     print(index, list_of_numbers)
        # print(index, list_of_numbers)
        index += 1

    mex = list_of_numbers.index(0)+1
    return mex


test_cases = [[3, 4, -1, 1],
              [1, 2, 3, -40, 56]]
map(lambda x: print(get_mex_impurely(x)), test_cases)
