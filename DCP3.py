"""This problem was asked by Google.
Given the root to a binary tree, implement serialize(root), which serializes the tree into a string, and deserialize(s), which deserializes the string back into the tree.
For example, given the following Node class
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
The following test should pass:
node = Node('root', Node('left', Node('left.left')), Node('right'))
assert deserialize(serialize(node)).left.left.val == 'left.left'"""

import re


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right


class Tree:

    KEY_SEPERATOR = '$'
    NODE_END = ')'
    EMPTY_NODE = '#'
    REGEX = '(\$|\))'

    def __init__(self, root=None, tree_str=None):
        """Atmost one of root or tree_str is provided
        Otherwise the behaviour is undefined"""

        self.root = root
        if tree_str:
            self.token_list = [token for token in re.split(Tree.REGEX, tree_str) if token and token != Tree.KEY_SEPERATOR]
        else:
            self.token_list = None
        self.is_empty = True
        if root or tree_str:
            self.is_empty = False

    def is_empty(self):
        return self.is_empty

    @staticmethod
    def __serialize(root):
        if not root:
            return []
        token_list = [root.val]
        if not root.left and root.right:
            token_list.append(Tree.EMPTY_NODE)
        token_list.extend(Tree.__serialize(root.left))
        token_list.extend(Tree.__serialize(root.right))
        token_list.append(Tree.NODE_END)
        return token_list

    def __deserialize(self, start_index, end_index):
        """Assumes that the tree is non-empty
        returns the position of first match: when number of NODE_END
        is equal to number of KEY_SEPERATOR
        Also constructs a tree by deserializing the string
        and returns its root"""

        if start_index == end_index:
            return None, start_index

        if self.token_list[start_index] == Tree.EMPTY_NODE:
            return None, start_index+1

        if (start_index+1) >= end_index or \
            self.token_list[end_index-1] != Tree.NODE_END or \
            self.token_list[start_index] == Tree.NODE_END:
            raise Exception("Malformed string: ",self.token_list[start_index:end_index-1],
                            start_index, end_index, self.token_list[end_index-1], self.token_list[start_index + 1])

        root = Node(self.token_list[start_index])
        start_index += 1
        num_keys_minus_subtree_end = 1
        balanced_till = -1

        for index, token in enumerate(self.token_list[start_index:end_index]):
            if token == Tree.KEY_SEPERATOR:
                raise Exception("Found key separator in token list: ", self.token_list[start_index:end_index])
            elif token == Tree.NODE_END:
                num_keys_minus_subtree_end -= 1
                if num_keys_minus_subtree_end < 0:
                    raise Exception("Malformed string: ", self.token_list[start_index:end_index])
                elif num_keys_minus_subtree_end == 0:
                    balanced_till = start_index + index
                    break
            elif token != Tree.EMPTY_NODE: # not a meta token
                num_keys_minus_subtree_end += 1

        if balanced_till == -1:
            raise Exception("Malformed string: ", self.token_list[start_index-2:end_index])

        left_child, left_end_index = self.__deserialize(start_index, balanced_till)
        right_child, right_end_index = self.__deserialize(left_end_index, balanced_till)

        if left_child:
            print "left child of {} is {}".format(root.val, left_child.val)
        if right_child:
            print "right child of {} is {}".format(root.val, right_child.val)

        root.set_left(left_child)
        root.set_right(right_child)

        return root, balanced_till+1

    def get_root(self):

        if self.is_empty:
            return None

        if not self.root:
            self.root, valid_till = self.__deserialize(0, len(self.token_list))
            if valid_till != len(self.token_list):
                raise Exception("Malformed token string: ", self.token_list)

        return self.root

    def get_serialized_string(self):

        def convert_token(token):
            if token == Tree.KEY_SEPERATOR:
                raise Exception('key seperator found in token list')
            elif token == Tree.NODE_END:
                return token
            else:
                return token + Tree.KEY_SEPERATOR

        if self.is_empty:
            return ""

        if not self.token_list:
            self.token_list = Tree.__serialize(self.root)

        return ''.join(map(convert_token, self.token_list))

    @staticmethod
    def __are_equal(A, B):
        if (not A) and (not B):
            return True
        if not (A and B):
            return False
        return (A.val == B.val) and Tree.__are_equal(A.left, B.left) and Tree.__are_equal(A.right, B.right)

    def equals(self, other_tree):
        return Tree.__are_equal(self.get_root(), other_tree.get_root())


#test 1
A = Node('A')
B = Node('B')
C = Node('C')
D = Node('D')
E = Node('E')
F = Node('F')
G = Node('G')
A.set_left(B)
A.set_right(C)
B.set_left(D)
B.set_right(E)
C.set_right(F)
F.set_right(G)
tree_A = Tree(root=A)
tree_str = tree_A.get_serialized_string()
print tree_A.token_list
print tree_str
A2 = Tree(tree_str=tree_str)
A2.get_root()
print A2.token_list
print A2.equals(tree_A)

# test 2
node_B = Node('B')
node_B.set_left(Node('C'))
node_C = Node('B')
node_C.set_right(Node('C'))
print Tree(root=node_B).equals(Tree(root=node_C))

# test 3
print Tree(root=Node('AS')).equals(Tree(tree_str="AS$#$)"))
