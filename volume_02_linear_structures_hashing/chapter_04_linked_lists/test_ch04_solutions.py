import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def walk(start, step, limit=50):
    out, node = [], start
    while node is not None and node.value is not None and len(out) < limit:
        out.append(node.value)
        node = getattr(node, step)
    return out


class TestThinkingProblems(unittest.TestCase):
    def test_correct_calls_keep_the_mirror(self) -> None:
        rng = random.Random(4)
        d, model = ex.DoublyLinkedList(), []
        for step in range(3000):
            if model and rng.random() < 0.45:
                k = rng.randrange(len(model))
                node = d.header.next
                for _ in range(k):
                    node = node.next
                self.assertEqual(d.remove(node), model.pop(k))
            else:
                k = rng.randint(0, len(model))
                before = d.header
                for _ in range(k):
                    before = before.next
                d.insert_between(step, before, before.next)
                model.insert(k, step)
            self.assertEqual(d.values(), model)
            self.assertEqual(d.values_backward(), model[::-1])

    def test_wrong_order_breaks_the_mirror(self) -> None:
        d = ex.DoublyLinkedList([25, 47, 63])
        d.insert_between(58, d.find(63), d.find(25))
        self.assertEqual(walk(d.header.next, "next", 8), [25, 47, 63, 58, 25, 47, 63, 58])

    def test_splice_between_lists(self) -> None:
        a, b = ex.DoublyLinkedList(["Ana", "Ben", "Cai", "Dev"]), ex.DoublyLinkedList(["Eve", "Fay"])
        sol.splice(a.find("Ben"), a.find("Cai"), b.find("Eve"))
        self.assertEqual((a.values(), a.values_backward()), (["Ana", "Dev"], ["Dev", "Ana"]))
        self.assertEqual((b.values(), b.values_backward()), (["Eve", "Ben", "Cai", "Fay"], ["Fay", "Cai", "Ben", "Eve"]))

    def test_splice_smallest_and_edges(self) -> None:
        a, b = ex.DoublyLinkedList(["Ana"]), ex.DoublyLinkedList()
        n = a.find("Ana")
        sol.splice(n, n, b.header)                       # one-node run into an empty list
        self.assertEqual((a.values(), b.values(), b.values_backward()), ([], ["Ana"], ["Ana"]))
        c = ex.DoublyLinkedList([1, 2, 3, 4, 5])
        sol.splice(c.find(4), c.find(5), c.header)       # within one list, to the front
        self.assertEqual((c.values(), c.values_backward()), ([4, 5, 1, 2, 3], [3, 2, 1, 5, 4]))
        sol.splice(c.find(4), c.find(4), c.find(3))      # to the back
        self.assertEqual((c.values(), c.values_backward()), ([5, 1, 2, 3, 4], [4, 3, 2, 1, 5]))

    def test_delete_by_copy_fails(self) -> None:
        shelf = ex.LinkedList([12, 25, 47, 63])
        with self.assertRaises(ValueError):
            sol.delete_by_copy(shelf.find(63))
        held = shelf.find(47)
        sol.delete_by_copy(shelf.find(25))
        shelf.insert_after(held, 50)
        self.assertEqual(shelf.values(), [12, 47, 63])


if __name__ == "__main__":
    unittest.main()
