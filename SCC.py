from collections import defaultdict

adjacency_list = {
    1: [2],
    2: [4, 5],
    3: [2],
    4: [1, 3],
    5: [6],
    6: [7],
    7: [5],
    8: [5],
    9: []
}

begin_time = {}
finish_time = {}


def first_dfs(adjacency_list):
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


def get_reverse_adjacency_list(adjacency_list):
    rev_graph = defaultdict(list)
    for u, neighbours in adjacency_list.items():
        for v in neighbours:
            rev_graph[v].append(u)

    return rev_graph


visited = set()


def get_SCC(u, rev_adj_list):
    SCC = set()

    def dfs(u):
        visited.add(u)
        SCC.add(u)
        for v in rev_adj_list[u]:
            if v not in visited:
                dfs(v)

    dfs(u)
    return SCC


vertex_order = first_dfs(adjacency_list)
print(vertex_order)
reverse_adj_list = get_reverse_adjacency_list(adjacency_list)
print(reverse_adj_list)
SCCs = []
for u in vertex_order:
    if u not in visited:
        SCCs.append(get_SCC(u, reverse_adj_list))


print(SCCs)
