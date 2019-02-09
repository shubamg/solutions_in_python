"""This problem was asked by Facebook.
A builder is looking to build a row of N houses that can be of K different colors.
He has a goal of minimizing cost while ensuring that no two neighboring houses are of the same color.
Given an N by K matrix where the nth row and kth column represents the cost
to build the nth house with kth color,
return the minimum cost which achieves this goal."""

from __future__ import print_function
from collections import deque


class DpState:

    INITIAL_COST = 10000000

    def __init__(self, prev_min_path=[], prev_second_min_path=[]):
        self.mincost = 10000000
        self.minpath = prev_min_path
        self.minpath.append(-1)
        self.optimal_color = -1
        self.second_optimal_color = -1
        self.secondmincost = 10000000
        self.secondminpath = prev_second_min_path
        self.secondminpath.append(-1)

    def update(self, color, cost):
        if cost <= self.mincost:
            self.secondmincost = self.mincost
            self.secondminpath[-1] = self.minpath[-1]
            self.second_optimal_color = self.optimal_color
            self.mincost = cost
            self.minpath[-1] = color
            self.optimal_color = color

        elif cost <= self.secondmincost:
            self.secondmincost = cost
            self.secondminpath[-1] = color
            self.second_optimal_color = color

    def get_optimal_color(self):
        return self.optimal_color


def f(matrix, n):
    # Assume one row per house
    if n == 0:
        new_state = DpState()
        for color, cost in enumerate(matrix[n]):
            new_state.update(color, cost)
        return new_state

    prev_state = f(matrix, n-1)
    new_state = DpState(prev_state.minpath, prev_state.secondminpath)
    for color, cost in enumerate(matrix[n]):
        if color == prev_state.get_optimal_color():
            new_state.update(color, cost + prev_state.secondmincost)
        else:
            new_state.update(color, cost + prev_state.mincost)
    return new_state


def get_optimal_coloring(matrix):
    result = f(matrix, len(matrix)-1)
    input = ''
    for row in matrix:
        input += ', '.join((str(x) for x in row))
        input += '\n'

    return (input + '\n' + str(result.mincost) +
    '\n' + ', '.join((str(x) for x in result.minpath)) + '\n\n')


inputs = [[[1,2,3,4],
        [4, 6, 2, 7],
        [5, 8, 3, 6]]]
map(lambda x: print(get_optimal_coloring(x)), inputs)

