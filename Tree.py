from parse import compile


class Node:

    CHILD_INDICATOR = '|->'

    def __init__(self, x):
        self.val = x
        self.children = []
        self.parent = None

    def dfs(self, prefix, is_last_child=False):
        print(prefix, self.val)

        replacement = '|  ' if not is_last_child else '   '
        new_prefix = prefix.replace(Node.CHILD_INDICATOR, replacement) + ' ' * len(self.val)
        prefix_for_children  = new_prefix + Node.CHILD_INDICATOR
        empty_line = new_prefix + '|  '

        num_children_of_prev_child = 0
        for index, child in enumerate(self.children):
            if num_children_of_prev_child > 0:
                print(empty_line)
            num_children_of_prev_child = child.dfs(prefix_for_children, index+1 == len(self.children))

        return len(self.children)

    def __repr__(self):
        return self.val


class Tree:
    def __init__(self, edge_list, root):
        self.vertices = {}
        self.root = self.vertices.setdefault(root, Node(root))
        for edge in edge_list:
            s = self.vertices.setdefault(edge.s, Node(edge.s))
            t = self.vertices.setdefault(edge.t, Node(edge.t))
            t.parent = s
            s.children.append(t)
        pass

    def dfs(self):
        self.root.dfs('', True)


class Edge:

    style = compile('{s}->{t}')

    def __init__(self, edge_line):
        p = Edge.style.parse(edge_line)
        self.s, self.t = p['s'], p['t']


edge_list_str = """A->B
B->D
B->E
A->C
C->F
F->G
F->H
F->I"""

tree = Tree((Edge(x) for x in edge_list_str.split('\n')), 'A')
tree.dfs()
