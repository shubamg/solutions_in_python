"""This problem was asked by Google.
Implement locking in a binary tree.
A binary tree node can be locked or unlocked only if all of its descendants or ancestors are not locked.
Design a binary tree node class with the following methods:
is_locked, which returns whether the node is locked
lock, which attempts to lock the node. If it cannot be locked,
then it should return false. Otherwise, it should lock it and return true.
unlock, which unlocks the node. If it cannot be unlocked, then it should return false.
Otherwise, it should unlock it and return true.
You may augment the node to add parent pointers or any other property you would like.
You may assume the class is used in a single-threaded program, so there is no need for actual locks or mutexes.
Each method should run in O(h), where h is the height of the tree."""

from parse import compile


class Node:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None
        self.parent = None
        self.count_descendants_locked = 0
        self.is_locked = False

    def can_change_state(self):
        can_change_state = (self.count_descendants_locked == 0)
        ancestor = self.parent
        while ancestor and can_change_state:
            can_change_state = can_change_state and not ancestor.is_locked
            ancestor = ancestor.parent
        return can_change_state

    def set_state(self, to_lock):
        ancestor = self.parent
        if self.can_change_state():
            while ancestor:
                ancestor.count_descendants_locked += (1 if to_lock else -1)
                ancestor = ancestor.parent
            self.is_locked = to_lock
        return self.is_locked == to_lock

    def lock(self):
        return "Attempt to lock {0}. {0} is now locked: {1}".format(self.val, self.set_state(True))

    def unlock(self):
        return "Attempt to unlock {0}. {0} is now unlocked: {1}".format(self.val, self.set_state(False))


class Edge:

    style = compile('{s}-{direction}>{t}')
    LEFT = 'L'
    RIGHT = 'R'

    def __init__(self, edge_line):
        p = Edge.style.parse(edge_line)
        self.s, self.t, self.direction = p['s'], p['t'], p['direction']


class Tree:
    def __init__(self, edge_list, root):
        self.vertices = {}
        self.root = self.vertices.setdefault(root, Node(root))
        for edge in edge_list:
            s = self.vertices.setdefault(edge.s, Node(edge.s))
            t = self.vertices.setdefault(edge.t, Node(edge.t))
            t.parent = s
            if edge.direction == Edge.LEFT:
                s.left_child = t
            else:
                s.right_child = t

    def lock(self, key):
        return self.vertices[key].lock()

    def unlock(self, key):
        return self.vertices[key].unlock()


edge_list_str = """A-L>B
B-L>D
B-R>E
A-R>C
C-R>F
F-L>G
F-R>H"""

tree = Tree((Edge(x) for x in edge_list_str.split('\n')), 'A')
operations = (tree.lock('A'), tree.lock('G'), tree.unlock('G'), tree.lock('A'),
              tree.unlock('A'), tree.lock('B'), tree.lock('D'),
              tree.lock('C'), tree.lock('A'), tree.unlock('B'),
              tree.lock('A'), tree.unlock('C'), tree.lock('A'))
for operation in operations:
    print(operation)
