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

    def __init__(self, on_change=lambda x, y, z: None):
        self.heap = []
        self.elem_to_node: Dict[Any, HeapNode] = {}
        self.on_change = on_change

    def push_or_update(self, elem, key):
        self.delete(elem)
        node = HeapNode(elem, key)
        self.elem_to_node[elem] = node
        self.on_change(elem, None, key)
        heapq.heappush(self.heap, node)

    def pop(self):
        while self.heap:
            node: HeapNode = heapq.heappop(self.heap)
            if node.is_valid():
                old_key = node.get_key()
                elem = node.get_elem()
                del self.elem_to_node[elem]
                self.on_change(elem, old_key, None)
                return node
        return None

    def __len__(self):
        return len(self.elem_to_node)

    def delete(self, elem):
        if elem in self.elem_to_node:
            old_key = self.elem_to_node[elem].get_key()
            self.elem_to_node[elem].invalidate()
            del self.elem_to_node[elem]
        else:
            old_key = None
        self.on_change(elem, old_key, None)

    def __contains__(self, item):
        return item in self.elem_to_node

    def __repr__(self):
        # Return detailed info for debugging.
        return (f"{self.__class__.__name__}(heap={[node.key for node in self.heap if node.is_valid()]}")


class TopKSelector:
    def __init__(self, k, on_change=lambda x, y, z: None, key_negator=lambda x: -x):
        assert k >= 0
        self.k = k
        self.key_negator = key_negator
        self.large_elems = AdaptableHeap(on_change)
        self.other_elems = AdaptableHeap()

    def delete(self, elem):
        if elem not in self.large_elems:
            self.other_elems.delete(elem)
            return
        self.large_elems.delete(elem)
        node = self.other_elems.pop()
        if node:
            new_key = self.key_negator(node.get_key())
            self.large_elems.push_or_update(node.get_elem(), new_key)

    def add_or_update(self, elem, key):
        self.delete(elem)
        self.large_elems.push_or_update(elem, key)
        if len(self.large_elems) == self.k + 1:
            node = self.large_elems.pop()
            new_key = self.key_negator(node.get_key())
            self.other_elems.push_or_update(node.get_elem(), new_key)

    def __contains__(self, item):
        return item in self.large_elems

    def __repr__(self):
        return (f"{self.__class__.__name__}(k={self.k}, "
                f"large_elems={repr(self.large_elems)}, "
                f"other_elems={repr(self.other_elems)})")


class TestAdaptableHeap(unittest.TestCase):

    def setUp(self):
        # Log will collect tuples of (elem, old_key, new_key)
        self.log = []

        def logger(elem, old_key, new_key) -> None:
            self.log.append((elem, old_key, new_key))

        self.heap = AdaptableHeap(on_change=logger)

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

    def test_push_or_update_new(self):
        # For a new element, delete() is called first.
        # Since the element doesn't exist, delete() logs (elem, None, None).
        # Then push_or_update logs (elem, None, key).
        self.heap.push_or_update("a", 10)
        self.assertEqual(self.log, [("a", None, None), ("a", None, 10)])
        self.log.clear()

    def test_push_or_update_update(self):
        # First add the element.
        self.heap.push_or_update("a", 10)
        self.log.clear()
        # Now update "a". Since it exists, delete() finds it and logs (elem, old_key, None).
        # Then push_or_update logs (elem, None, new_key).
        self.heap.push_or_update("a", 20)
        self.assertEqual(self.log, [("a", 10, None), ("a", None, 20)])
        self.log.clear()

    def test_delete_existing(self):
        self.heap.push_or_update("a", 10)
        self.log.clear()
        self.heap.delete("a")
        # Since "a" exists, delete() logs (a, 10, None).
        self.assertEqual(self.log, [("a", 10, None)])
        self.log.clear()

    def test_delete_nonexistent(self):
        self.heap.delete("b")
        # For a non-existent element, delete() logs (b, None, None).
        self.assertEqual(self.log, [("b", None, None)])
        self.log.clear()

    def test_pop(self):
        self.heap.push_or_update("a", 10)
        self.log.clear()
        node = self.heap.pop()
        # pop() should log (a, 10, None) when returning the valid node.
        self.assertIsNotNone(node)
        self.assertEqual(node.get_elem(), "a")
        self.assertEqual(node.get_key(), 10)
        self.assertEqual(self.log, [("a", 10, None)])
        self.log.clear()

    def test_multiple_operations(self):
        # Test a sequence of operations.
        self.heap.push_or_update("a", 10)  # Logs: ("a", None, None), ("a", None, 10)
        self.heap.push_or_update("b", 20)  # Logs: ("b", None, None), ("b", None, 20)
        self.heap.push_or_update("c", 15)  # Logs: ("c", None, None), ("c", None, 15)
        expected_initial = [("a", None, None), ("a", None, 10),
                            ("b", None, None), ("b", None, 20),
                            ("c", None, None), ("c", None, 15)]
        self.assertEqual(self.log, expected_initial)
        self.log.clear()

        # Update "b" from 20 to 25.
        self.heap.push_or_update("b", 25)
        # Should log: ("b", 20, None) from delete and ("b", None, 25) from push.
        self.assertEqual(self.log, [("b", 20, None), ("b", None, 25)])
        self.log.clear()

        # Delete "a".
        self.heap.delete("a")
        self.assertEqual(self.log, [("a", 10, None)])
        self.log.clear()

        # Pop one element. We'll verify that the change log corresponds to the popped element.
        node = self.heap.pop()
        # The log for pop should contain exactly one entry (elem, key, None) for the popped node.
        self.assertEqual(len(self.log), 1)
        popped_log = self.log[0]
        self.assertEqual(popped_log[0], node.get_elem())
        self.assertEqual(popped_log[1], node.get_key())
        self.assertEqual(popped_log[2], None)
        self.log.clear()


class TestTopKSelector(unittest.TestCase):

    def setUp(self):
        # Create a TopKSelector with k=3 and a no-op change_log callback.
        self.topk = TopKSelector(3)

    def test_basic_membership_and_top_group(self):
        # Add several elements. For k=3, the selector should keep the three highest keys.
        # We assume higher key values are "better".
        self.topk.add_or_update('a', 10)
        self.topk.add_or_update('b', 20)
        self.topk.add_or_update('c', 15)
        # At this point, the top group (i.e. large_elems) has 'a', 'b', 'c'
        self.assertIn('a', self.topk)
        self.assertIn('b', self.topk)
        self.assertIn('c', self.topk)

        # Add an element with a very low key; it should be demoted.
        self.topk.add_or_update('d', 5)
        # The lowest element among the four should be bumped out.
        # In this scenario, 'd' has the lowest key so it should not be in the top group.
        self.assertNotIn('d', self.topk)
        # The others remain.
        self.assertIn('a', self.topk)
        self.assertIn('b', self.topk)
        self.assertIn('c', self.topk)

        # Now add an element with a high key so that one candidate gets bumped.
        self.topk.add_or_update('e', 25)
        # Now the top three should be the ones with the highest keys.
        # Expected: 'b' (20), 'c' (15), and 'e' (25) remain in the top group,
        # while the lowest ('a' with 10) is bumped into the auxiliary heap.
        self.assertIn('b', self.topk)
        self.assertIn('c', self.topk)
        self.assertIn('e', self.topk)
        self.assertNotIn('a', self.topk)
        self.assertNotIn('d', self.topk)

    def test_delete_from_top_promotes_candidate(self):
        # Build an initial state where some elements are in the top group and one is in the auxiliary group.
        self.topk.add_or_update('a', 10)
        self.topk.add_or_update('b', 20)
        self.topk.add_or_update('c', 15)
        self.topk.add_or_update('d', 5)  # 'd' will be demoted (sent to other_elems).
        # At this point, top group (large_elems) contains: 'a', 'b', 'c'
        # and other group (other_elems) contains: 'd'.

        # Delete a top element (say, 'b').
        self.topk.delete('b')
        # Because 'b' was in the top group, delete() attempts to promote a candidate from other_elems.
        # Here, 'd' should be promoted.
        self.assertNotIn('b', self.topk)
        self.assertIn('d', self.topk)
        # The remaining top group should now be 'a', 'c', and 'd'.
        self.assertIn('a', self.topk)
        self.assertIn('c', self.topk)

    def test_delete_from_auxiliary(self):
        # Add elements so that one ends up outside the top group.
        self.topk.add_or_update('a', 10)
        self.topk.add_or_update('b', 20)
        self.topk.add_or_update('c', 15)
        self.topk.add_or_update('d', 5)  # 'd' goes to auxiliary.
        # Confirm that 'd' is not in the top group.
        self.assertNotIn('d', self.topk)

        # Deleting an element that is not in the top group should simply remove it.
        self.topk.delete('d')
        self.assertNotIn('d', self.topk)
        # Top group remains unchanged.
        self.assertIn('a', self.topk)
        self.assertIn('b', self.topk)
        self.assertIn('c', self.topk)

    def test_update_promotes_element(self):
        # Add initial elements; one will be demoted.
        self.topk.add_or_update('a', 10)
        self.topk.add_or_update('b', 20)
        self.topk.add_or_update('c', 15)
        self.topk.add_or_update('d', 5)  # 'd' is demoted.
        self.assertNotIn('d', self.topk)

        # Now update 'd' with a higher key so that it qualifies for promotion.
        self.topk.add_or_update('d', 30)
        # The update removes any prior instance of 'd' from the auxiliary heap and then adds it to the top group.
        # As a result, one of the current top elements with a low key may be bumped.
        self.assertIn('d', self.topk)
        # Check that the top group now contains 3 items, and that 'd' is one of them.
        top_members = [item for item in ['a', 'b', 'c', 'd'] if item in self.topk]
        self.assertEqual(len(top_members), 3)
        self.assertIn('d', top_members)

    def test_k_zero_behavior(self):
        # For k == 0, the top group should never contain any elements.
        selector0 = TopKSelector(0)
        selector0.add_or_update('a', 10)
        self.assertNotIn('a', selector0)
        selector0.add_or_update('b', 20)
        self.assertNotIn('b', selector0)
        # Even updating an element doesn't put it in the top group.
        selector0.add_or_update('a', 30)
        self.assertNotIn('a', selector0)

    def test_multiple_mixed_operations(self):
        # Create a sequence of adds, updates, and deletes to verify the overall consistency.
        self.topk.add_or_update('a', 10)
        self.topk.add_or_update('b', 20)
        self.topk.add_or_update('c', 15)
        self.topk.add_or_update('d', 5)  # Demoted to auxiliary.
        self.topk.add_or_update('e', 25)  # Causes the smallest in top group to be bumped.
        # After these operations (with k=3), expected top group:
        # Highest three keys among: a(10), b(20), c(15), e(25) are: b, c, e.
        self.assertIn('b', self.topk)
        self.assertIn('c', self.topk)
        self.assertIn('e', self.topk)
        self.assertNotIn('a', self.topk)
        self.assertNotIn('d', self.topk)

        # Now update a previously demoted element so that it becomes top.
        self.topk.add_or_update('a', 30)
        # This update will remove 'a' from wherever it was and reinsert it.
        # With the new key, the top group should now be: a, b, e (assuming c with 15 gets bumped).
        self.assertIn('a', self.topk)
        self.assertIn('b', self.topk)
        self.assertIn('e', self.topk)
        # And 'c' and 'd' should not be in the top group.
        self.assertNotIn('c', self.topk)
        self.assertNotIn('d', self.topk)

    def test_change_log_callback(self):
        # Test that the change log callback is invoked.
        # We use a custom logger to record changes.
        log = []

        def logger(elem, old_key, new_key):
            log.append((elem, old_key, new_key))

        # Create a TopKSelector with k=2 and the custom logger.
        selector_with_log = TopKSelector(2, on_change=logger)
        # Perform an add_or_update for a new element.
        selector_with_log.add_or_update('a', 10)
        # Expect two log events: one from the internal delete() call (which logs (a, None, None))
        # and one from push_or_update (which logs (a, None, 10)).
        self.assertIn(('a', None, 10), log)

        log.clear()
        # Add a second element.
        selector_with_log.add_or_update('b', 20)
        log.clear()
        # Update 'a' to a higher key.
        selector_with_log.add_or_update('a', 30)
        # Expect that the logger recorded the deletion of the old 'a' (with key 10)
        # and then the push with key 30.
        # (Exact ordering can depend on internal calls, but we expect at least one log with ('a', 10, None)
        # and one with ('a', None, 30).)
        events = [event for event in log if event[0] == 'a']
        keys = {(old, new) for (_, old, new) in events}
        self.assertIn((10, None), keys)
        self.assertIn((None, 30), keys)

        log.clear()
        # Delete an element and verify that the callback is invoked.
        selector_with_log.delete('a')
        # Expect a log event showing that 'a' was deleted (its previous key should be 30).
        self.assertIn(('a', 30, None), log)


if __name__ == '__main__':
    unittest.main()
