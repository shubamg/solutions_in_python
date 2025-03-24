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

    def get_key(self):
        return self.key


class AdaptableHeap:

    def __init__(self):
        self.heap = []
        self.elem_to_node: Dict[Any, HeapNode] = {}

    def push_or_update(self, elem, key):
        if elem in self.elem_to_node:
            self.elem_to_node[elem].invalidate()
        node = HeapNode(elem, key)
        self.elem_to_node[elem] = node
        heapq.heappush(self.heap, node)

    def pop(self):
        while self.heap:
            node: HeapNode = heapq.heappop(self.heap)
            if node.is_valid():
                del self.elem_to_node[node.get_elem()]
                return node
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
        self.heap.push_or_update("apple", 5)
        self.heap.push_or_update("banana", 3)
        self.heap.push_or_update("cherry", 4)
        # The pop should return elements in increasing order of their key
        heap = self.heap
        self.assertEqual(heap.pop().get_elem(), "banana")
        adaptable_heap = self.heap
        self.assertEqual(adaptable_heap.pop().get_elem(), "cherry")
        heap1 = self.heap
        self.assertEqual(heap1.pop().get_elem(), "apple")
        # With no elements left, pop returns None.
        self.assertIsNone(self.heap.pop())

    def test_priority_update(self):
        # Test that pushing an element with a new key updates its priority.
        self.heap.push_or_update("alpha", 10)
        self.heap.push_or_update("beta", 20)
        # Update "alpha" with a lower key; the old entry is invalidated.
        self.heap.push_or_update("alpha", 5)
        # Now, only "alpha" (key 5) and "beta" (key 20) remain.
        heap = self.heap
        self.assertEqual(heap.pop().get_elem(), "alpha")
        adaptable_heap = self.heap
        self.assertEqual(adaptable_heap.pop().get_elem(), "beta")

    def test_len(self):
        self.assertEqual(len(self.heap), 0)
        self.heap.push_or_update("x", 1)
        self.assertEqual(len(self.heap), 1)
        self.heap.push_or_update("y", 2)
        self.assertEqual(len(self.heap), 2)
        self.heap.push_or_update("x", 20)
        self.assertEqual(len(self.heap), 2)
        heap = self.heap
        heap.pop().get_elem()
        self.assertEqual(len(self.heap), 1)
        adaptable_heap = self.heap
        adaptable_heap.pop().get_elem()
        self.assertEqual(len(self.heap), 0)

    def test_multiple_updates(self):
        # Test pushing multiple updates for the same element.
        self.heap.push_or_update("item", 100)
        # Update "item" with a lower key (this one will be invalidated by the next update)
        self.heap.push_or_update("item", 50)
        # Update "item" with a higher key; final valid node is key=200.
        self.heap.push_or_update("item", 200)
        # Only one valid instance should remain.
        self.assertEqual(len(self.heap), 1)
        # Since the final valid key is 200, "item" is popped.
        heap = self.heap
        self.assertEqual(heap.pop().get_elem(), "item")

    def test_accumulation_of_invalid_nodes(self):
        # Using only the public API, simulate many updates for a single element.
        # Even though each update invalidates the previous one, only one valid
        # instance should be present.
        for i in range(100):
            self.heap.push_or_update("dup", i)
            self.assertEqual(len(self.heap), 1)
        # Pop should return the valid "dup" element.
        heap = self.heap
        self.assertEqual(heap.pop().get_elem(), "dup")
        # After the valid element is popped, further pop() calls should return None.
        self.assertIsNone(self.heap.pop())
        self.assertEqual(len(self.heap), 0)

    def test_edge_case_behaviors(self):
        # Edge case: popping from an empty heap returns None.
        self.assertIsNone(self.heap.pop())

        # Edge case: pushing elements with equal keys.
        self.heap.push_or_update("a", 10)
        self.heap.push_or_update("b", 10)
        # Although order for equal keys is undefined, both should eventually be popped.
        heap2 = self.heap
        heap3 = self.heap
        popped = {heap2.pop().get_elem(), heap3.pop().get_elem()}
        self.assertEqual(popped, {"a", "b"})
        self.assertIsNone(self.heap.pop())

        # Edge case: multiple elements with interleaved updates.
        self.heap.push_or_update("x", 10)
        self.heap.push_or_update("y", 20)
        self.heap.push_or_update("x", 5)  # Update "x" with a lower key.
        self.heap.push_or_update("z", 15)
        # Expected pop order: "x" (5), then "z" (15), then "y" (20)
        heap = self.heap
        self.assertEqual(heap.pop().get_elem(), "x")
        adaptable_heap = self.heap
        self.assertEqual(adaptable_heap.pop().get_elem(), "z")
        heap1 = self.heap
        self.assertEqual(heap1.pop().get_elem(), "y")
        self.assertIsNone(self.heap.pop())

    def test_delete_existing(self):
        # Test that delete removes an element so that it won't be returned by pop.
        self.heap.push_or_update("a", 10)
        self.heap.push_or_update("b", 20)
        self.heap.push_or_update("c", 15)
        # Delete "b".
        self.heap.delete("b")
        # __len__ should reflect that "b" is gone.
        self.assertEqual(len(self.heap), 2)
        popped = []
        while True:
            node = self.heap.pop()
            if node is None:
                break
            popped.append(node.get_elem())
        self.assertNotIn("b", popped)
        # The remaining order should be "a" then "c" (by key order).
        self.assertEqual(popped, ["a", "c"])

    def test_delete_nonexistent(self):
        # Deleting an element that doesn't exist should do nothing.
        self.heap.push_or_update("x", 5)
        # Delete a non-existent element.
        self.heap.delete("nonexistent")
        self.assertEqual(len(self.heap), 1)
        heap = self.heap
        self.assertEqual(heap.pop().get_elem(), "x")
        self.assertIsNone(self.heap.pop())

    def test_delete_after_multiple_updates(self):
        # Push multiple updates for the same element and then delete it.
        self.heap.push_or_update("dup", 100)
        self.heap.push_or_update("dup", 50)
        self.heap.push_or_update("dup", 200)
        # Delete the element.
        self.heap.delete("dup")
        self.assertEqual(len(self.heap), 0)
        # Popping should not return the deleted element.
        self.assertIsNone(self.heap.pop())

    def test_membership_after_push(self):
        self.heap.push_or_update("apple", 5)
        self.assertIn("apple", self.heap)
        self.assertNotIn("banana", self.heap)

    def test_membership_after_pop(self):
        self.heap.push_or_update("apple", 5)
        self.heap.push_or_update("banana", 3)
        self.assertIn("apple", self.heap)
        self.assertIn("banana", self.heap)
        # Pop should remove the element from membership
        heap = self.heap
        popped = heap.pop().get_elem()
        self.assertNotIn(popped, self.heap)

    def test_membership_after_delete(self):
        self.heap.push_or_update("cherry", 4)
        self.assertIn("cherry", self.heap)
        self.heap.delete("cherry")
        self.assertNotIn("cherry", self.heap)


if __name__ == '__main__':
    unittest.main()
