"""This problem was asked by Snapchat.
Given an array of time intervals (start, end) for classroom lectures (possibly overlapping),
find the minimum number of rooms required.
For example, given [(30, 75), (0, 50), (60, 150)], you should return 2."""

from itertools import accumulate


def f(_input):
    def process_tuple(t):
        return [(t[0], -1), (t[1], 1)]

    end_points = []
    for t in _input:
        end_points.extend(process_tuple(t))
    end_points = sorted(end_points)
    return -min(list(accumulate(t[1] for t in end_points)))


print(f([(30, 75), (0, 50), (60, 150)]))
