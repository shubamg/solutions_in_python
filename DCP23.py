"""This problem was asked by Google.
You are given an M by N matrix consisting of booleans that represents a board.
Each True boolean represents a wall. Each False boolean represents a tile you can walk on.
Given this matrix, a start coordinate, and an end coordinate,
return the minimum number of steps required to reach the end coordinate from the start.
If there is no possible path, then return null. You can move up, left, down, and right.
You cannot move through walls. You cannot wrap around the edges of the board.
For example, given the following board:
[[f, f, f, f],
[t, t, f, t],
[f, f, f, f],
[f, f, f, f]]
and start = (3, 0) (bottom left) and end = (0, 0) (top left),
the minimum number of steps required to reach the end is 7,
since we would need to go through (1, 2)
because there is a wall everywhere else on the second row."""

from collections import deque


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def get_neighbours(self):
        neighbours = []
        for p in Point.two_D_movements:
            neighbours.append(self.add(p))
        return neighbours

    def __repr__(self):
        return '[{0}][{1}] = ({1},{0})'.format(self.y, self.x)


Point.two_D_movements = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]


def bfs(is_wall, start, end):
    queue = deque()
    N = len(is_wall)
    M = len(is_wall[0])
    INF = -1
    distance = [[INF] * M for i in range(N)]

    def is_in_grid(point):
        return (0 <= point.x < M) and (0 <= point.y < N)

    def add_to_queue(v, d):
        print("Adding {} to queue at distance {}".format(v, d))
        distance[v.y][v.x] = d
        queue.appendleft(v)

    def get_distance(u):
        return distance[u.y][u.x]
    
    def can_explore(u):
        return is_in_grid(u) and get_distance(u) == INF and not is_wall[u.y][u.x]

    add_to_queue(start, 0)
    reached_end = False
    while len(queue) and not reached_end:
        v = queue.pop()
        neighbours = (u for u in v.get_neighbours() if can_explore(u))
        for u in neighbours:
            add_to_queue(u, get_distance(v) + 1)
            if u == end:
                reached_end = True
                break
                
    return get_distance(end)
        
        
print(bfs(
    [[False, False, False, False],
    [True, True, False, True],
    [False, False, False, False],
    [False, False, False, False]],
    Point(0, 3), Point(0, 0)))


