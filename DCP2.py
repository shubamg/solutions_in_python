"""This problem was asked by Uber.
Given an array of integers, return a new array such that each element at index i of the new array is the product of all the numbers in the original array except the one at i.
For example, if our input was [1, 2, 3, 4, 5], the expected output would be [120, 60, 40, 30, 24]. If our input was [3, 2, 1], the expected output would be [2, 3, 6].
Follow-up: what if you can't use division?"""
from __future__ import print_function


def get_prefix_product(input_arr):
    product = 1
    result = []
    for num in input_arr:
        product *= num
        result.append(product)
    return result


def f(input_arr):
    length = len(input_arr)
    modified_arr = [1]+input_arr+[1]
    left_prod = get_prefix_product(modified_arr)
    modified_arr.reverse()
    right_prod = get_prefix_product(modified_arr)
    right_prod.reverse()
    result = []
    for i in xrange(length):
        result.append(left_prod[i]*right_prod[i+2])
    return zip(input_arr, result)


inputs = [[1, 2, 3, 4, 5],
          [1234, 567, -90],
          [1, 2345]]
map(lambda x: print(f(x)), inputs)
