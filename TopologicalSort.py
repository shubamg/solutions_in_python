# from collections import namedtuple

adjacency_list = {
    1: [2],
    2: [5],
    3: [2],
    4: [1, 3],
    5: [6],
    6: [7],
    7: [],
    8: [5],
    9: []
}

begin_time = {}
finish_time = {}


def topo(adjacency_list):
    t = 0

    def visit(u):
        nonlocal t
        begin_time[u] = t
        t += 1
        for v in adjacency_list[u]:
            if v not in begin_time:
                visit(v)
        finish_time[u] = t
        t += 1

    for v in adjacency_list.keys():
        if v not in begin_time:
            visit(v)

    return sorted(finish_time, key = finish_time.get, reverse=True)


print(topo(adjacency_list))
