"""This problem was asked by Google.
Given two singly linked lists that intersect at some point, find the intersecting node.
The lists are non-cyclical.
For example, given A = 3 -> 7 -> 8 -> 10 and B = 99 -> 1 -> 8 -> 10,
return the node with value 8.
In this example, assume nodes with the same value are the exact same node objects.
Do this in O(M + N) time (where M and N are the lengths of the lists) and constant space."""

from __future__ import print_function


class Node:
    def __init__(self, val):
        self.val = val
        self.next_node = None

    def __repr__(self):
        return str(self.val)


class SinglyLinkedList:

    def __init__(self, values=[]):
        self.head = None
        self.tail = None
        for value in values:
            self.append(value)

    def append(self, val):
        previous_tail = self.tail
        self.tail = Node(val)
        if previous_tail:
            previous_tail.next_node = self.tail
        else:
            self.head = self.tail

    def __repr__(self):
        repr = []
        node = self.head
        while node:
            repr.append(node.val)
            node = node.next_node
        return str(repr)


inputs = [[1, 2, 3, 4, 5, 7, 8],
          [0, 46, 5, 7, 8],
          [345, 567, 89, 5678, 78, 95]]

singly_linked_lists = map(lambda x: SinglyLinkedList(x), inputs)
for index, list_ in enumerate(singly_linked_lists):
    print("list", str(index), ": ", list_)
print("#"*100, "\n")

heads = map(lambda x: getattr(x, 'head'), singly_linked_lists)


def f(index1, index2):
    def get_list_len(head):
        ptr = head
        len_ = 0
        while ptr:
            len_ += 1
            ptr = ptr.next_node
        return len_

    print("Lists ", index1, " and ", index2)
    head1 = heads[index1]
    head2 = heads[index2]
    len1 = get_list_len(head1)
    len2 = get_list_len(head2)
    short = head1
    long_ = head2
    if len1 > len2:
        short, long_ = head2, head1
    diff = max(len1, len2) - min(len1, len2)
    while diff:
        long_ = long_.next_node
        diff -= 1
    while long_ and long_.val != short.val:
        long_ = long_.next_node
        short = short.next_node

    if long_:
        print("First common node is ", long_.val)
    else:
        print("Lists do not intersect")
    print("#"*100, "\n")


f(0, 1)
f(1, 2)