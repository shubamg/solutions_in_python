from collections import namedtuple
from pprint import pprint

BEGIN_DIGRAPH = 'digraph structs {'
END_DIGRAPH = '}'


class Edge(namedtuple('Edge', ['s', 't', 'w'])):
    def __repr__(self):
        # return "From {0} to {1} with w = {2:+010.4f}".format(self.s, self.t, self.w)
        # return "From {0} to {1} with w = {2:+d}".format(self.s, self.t, self.w)
        return '{0.s} -> {0.t} [label = "{0.w:+d}"];'.format(self)


def createDOT(edges):
    output = [BEGIN_DIGRAPH]
    for edge in edges:
        output.append(str(edge))
    output.append(END_DIGRAPH)
    return output


edge_list = [
    ('A', 'B', 2),
    ('B', 'C', 3),
    ('C', 'D', -1),
    ('D', 'E', 5),
    ('E', 'C', -5),
    ('A', 'E', 4),
    ("A", 'F', 1),
    ('F', 'G', 50)
]

edge_list = [Edge(*x) for x in edge_list]
# print('\n'.join(((str(x) for x in edge_list))))

with open('BellmanFord.dot', 'w') as f:
    f.write('\n'.join(createDOT(edge_list)))


def BellManFord(edge_list, source):
    INF = 1000000
    distance = {u:INF for e in edge_list for u in e[:2]}
    parent = {u:None for e in edge_list for u in e[:2]}
    distance[source] = 0
    V = len(distance)
    neg_cycle = []
    for i in range(V-1):
        for edge in edge_list:
            if distance[edge.t] > distance[edge.s] + edge.w:
                distance[edge.t] = distance[edge.s] + edge.w
                parent[edge.t] = edge.s

    for edge in edge_list:
        if distance[edge.t] > distance[edge.s] + edge.w:
            print("Graph contains a negative-weight cycle reachable from source")
            vertices_of_neg_cycle = set()
            neg_cycle_vertex = edge.t
            while neg_cycle_vertex not in vertices_of_neg_cycle:
                vertices_of_neg_cycle.add(neg_cycle_vertex)
                neg_cycle.append(neg_cycle_vertex)
                neg_cycle_vertex = parent[neg_cycle_vertex]
            neg_cycle.reverse()

    return distance, parent, neg_cycle


dis, parent, neg_cycle = BellManFord(edge_list, 'A')
print("Distances:")
pprint(dis, width=1)
print("Predecessors:")
pprint(parent, width=1)
print("Negative cycle:")
print('->'.join(neg_cycle))
