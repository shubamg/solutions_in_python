import heapq
import unittest
from typing import Dict, Any


class HeapNode:

    def __init__(self, elem, key):
        self.elem = elem
        self.key = key
        self.valid = True

    def is_valid(self):
        return self.valid

    def invalidate(self):
        self.valid = False

    def __lt__(self, other):
        return self.key < other.key

    def get_elem(self):
        return self.elem

class AdaptableHeap:

    def __init__(self):
        self.heap = []
        self.elem_to_node: Dict[Any, HeapNode] = {}

    def push(self, elem, key):
        if elem in self.elem_to_node:
            self.elem_to_node[elem].invalidate()
        node = HeapNode(elem, key)
        self.elem_to_node[elem] = node
        heapq.heappush(self.heap, node)

    def pop(self):
        while self.heap:
            node: HeapNode = heapq.heappop(self.heap)
            if node.is_valid():
                elem = node.get_elem()
                del self.elem_to_node[elem]
                return elem
        return None

    def __len__(self):
        return len(self.elem_to_node)

    def delete(self, elem):
        if elem in self.elem_to_node:
            self.elem_to_node[elem].invalidate()
            del self.elem_to_node[elem]

    def __contains__(self, item):
        return item in self.elem_to_node

    def __repr__(self):
        # Return detailed info for debugging.
        return (f"{self.__class__.__name__}(heap={[node.key for node in self.heap]}, "
                f"valid_elements={list(self.elem_to_node.keys())})")

class TestAdaptableHeap(unittest.TestCase):

    def setUp(self):
        self.heap = AdaptableHeap()

    def test_push_and_pop_order(self):
        # Insert a few items with different keys
        self.heap.push("apple", 5)
        self.heap.push("banana", 3)
        self.heap.push("cherry", 4)
        # The pop should return elements in increasing order of their key
        self.assertEqual(self.heap.pop(), "banana")
        self.assertEqual(self.heap.pop(), "cherry")
        self.assertEqual(self.heap.pop(), "apple")
        # With no elements left, pop returns None.
        self.assertIsNone(self.heap.pop())

    def test_priority_update(self):
        # Test that pushing an element with a new key updates its priority.
        self.heap.push("alpha", 10)
        self.heap.push("beta", 20)
        # Update "alpha" with a lower key; the old entry is invalidated.
        self.heap.push("alpha", 5)
        # Now, only "alpha" (key 5) and "beta" (key 20) remain.
        self.assertEqual(self.heap.pop(), "alpha")
        self.assertEqual(self.heap.pop(), "beta")

    def test_len(self):
        self.assertEqual(len(self.heap), 0)
        self.heap.push("x", 1)
        self.assertEqual(len(self.heap), 1)
        self.heap.push("y", 2)
        self.assertEqual(len(self.heap), 2)
        self.heap.push("x", 20)
        self.assertEqual(len(self.heap), 2)
        self.heap.pop()
        self.assertEqual(len(self.heap), 1)
        self.heap.pop()
        self.assertEqual(len(self.heap), 0)

    def test_multiple_updates(self):
        # Test pushing multiple updates for the same element.
        self.heap.push("item", 100)
        # Update "item" with a lower key (this one will be invalidated by the next update)
        self.heap.push("item", 50)
        # Update "item" with a higher key; final valid node is key=200.
        self.heap.push("item", 200)
        # Only one valid instance should remain.
        self.assertEqual(len(self.heap), 1)
        # Since the final valid key is 200, "item" is popped.
        self.assertEqual(self.heap.pop(), "item")

    def test_accumulation_of_invalid_nodes(self):
        # Using only the public API, simulate many updates for a single element.
        # Even though each update invalidates the previous one, only one valid
        # instance should be present.
        for i in range(100):
            self.heap.push("dup", i)
            self.assertEqual(len(self.heap), 1)
        # Pop should return the valid "dup" element.
        self.assertEqual(self.heap.pop(), "dup")
        # After the valid element is popped, further pop() calls should return None.
        self.assertIsNone(self.heap.pop())
        self.assertEqual(len(self.heap), 0)

    def test_edge_case_behaviors(self):
        # Edge case: popping from an empty heap returns None.
        self.assertIsNone(self.heap.pop())

        # Edge case: pushing elements with equal keys.
        self.heap.push("a", 10)
        self.heap.push("b", 10)
        # Although order for equal keys is undefined, both should eventually be popped.
        popped = {self.heap.pop(), self.heap.pop()}
        self.assertEqual(popped, {"a", "b"})
        self.assertIsNone(self.heap.pop())

        # Edge case: multiple elements with interleaved updates.
        self.heap.push("x", 10)
        self.heap.push("y", 20)
        self.heap.push("x", 5)  # Update "x" with a lower key.
        self.heap.push("z", 15)
        # Expected pop order: "x" (5), then "z" (15), then "y" (20)
        self.assertEqual(self.heap.pop(), "x")
        self.assertEqual(self.heap.pop(), "z")
        self.assertEqual(self.heap.pop(), "y")
        self.assertIsNone(self.heap.pop())


    def test_delete_existing(self):
        # Test that delete removes an element so that it won't be returned by pop.
        self.heap.push("a", 10)
        self.heap.push("b", 20)
        self.heap.push("c", 15)
        # Delete "b".
        self.heap.delete("b")
        # __len__ should reflect that "b" is gone.
        self.assertEqual(len(self.heap), 2)
        popped = []
        while True:
            elem = self.heap.pop()
            if elem is None:
                break
            popped.append(elem)
        self.assertNotIn("b", popped)
        # The remaining order should be "a" then "c" (by key order).
        self.assertEqual(popped, ["a", "c"])

    def test_delete_nonexistent(self):
        # Deleting an element that doesn't exist should do nothing.
        self.heap.push("x", 5)
        # Delete a non-existent element.
        self.heap.delete("nonexistent")
        self.assertEqual(len(self.heap), 1)
        self.assertEqual(self.heap.pop(), "x")
        self.assertIsNone(self.heap.pop())

    def test_delete_after_multiple_updates(self):
        # Push multiple updates for the same element and then delete it.
        self.heap.push("dup", 100)
        self.heap.push("dup", 50)
        self.heap.push("dup", 200)
        # Delete the element.
        self.heap.delete("dup")
        self.assertEqual(len(self.heap), 0)
        # Popping should not return the deleted element.
        self.assertIsNone(self.heap.pop())

    def test_membership_after_push(self):
        self.heap.push("apple", 5)
        self.assertIn("apple", self.heap)
        self.assertNotIn("banana", self.heap)

    def test_membership_after_pop(self):
        self.heap.push("apple", 5)
        self.heap.push("banana", 3)
        self.assertIn("apple", self.heap)
        self.assertIn("banana", self.heap)
        # Pop should remove the element from membership
        popped = self.heap.pop()
        self.assertNotIn(popped, self.heap)

    def test_membership_after_delete(self):
        self.heap.push("cherry", 4)
        self.assertIn("cherry", self.heap)
        self.heap.delete("cherry")
        self.assertNotIn("cherry", self.heap)

if __name__ == '__main__':
    unittest.main()