"""This problem was asked by Google.
Given an array of integers and a number k, where 1 <= k <= length of the array,
compute the maximum values of each subarray of length k.
For example, given array = [10, 5, 2, 7, 8, 7] and k = 3, we should get: [10, 7, 8, 8], since:
10 = max(10, 5, 2)
7 = max(5, 2, 7)
8 = max(2, 7, 8)
8 = max(7, 8, 7)
Do this in O(n) time and O(k) space.
You can modify the input array in-place and you do not need to store the results.
You can simply print them out as you compute them."""

from __future__ import print_function
from collections import deque


def f(input, k):
    d = deque()
    moving_max = []
    for index, element in enumerate(input):
        while d and d[0] <= index - k:
            d.popleft()
        while d and input[d[-1]] <= element:
            d.pop()
        d.append(index)
        if index >= k-1:
            moving_max.append(input[d[0]])
    return moving_max


inputs = [([10, 5, 2, 7, 8, 7], 3),
          ([100, 500, -400, 29, 686], 2)]
map(lambda x: print(f(x[0], x[1])), inputs)
