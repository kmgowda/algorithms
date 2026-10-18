import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol
from ch06_examples import DoublyLinkedList, build


def check_links(test: unittest.TestCase, dll: DoublyLinkedList) -> None:
    forward = list(dll)
    test.assertEqual(list(dll.backwards()), forward[::-1])
    test.assertEqual(len(forward), len(dll))


def make_cycle(values: list[int], loop_to: int) -> ex.Node:
    head = build(values)
    nodes = []
    node = head
    while node is not None:
        nodes.append(node)
        node = node.next
    nodes[-1].next = nodes[loop_to]
    return head  # type: ignore[return-value]


class TestDoubly(unittest.TestCase):
    def test_against_model(self) -> None:
        rng = random.Random(4)
        dll, model = DoublyLinkedList(), []
        for _ in range(3000):
            op = rng.random()
            if op < 0.3:
                v = rng.randint(0, 9)
                dll.push_back(v)
                model.append(v)
            elif op < 0.55:
                v = rng.randint(0, 9)
                dll.push_front(v)
                model.insert(0, v)
            elif op < 0.78 and model:
                self.assertEqual(dll.pop_back(), model.pop())
            elif model:
                self.assertEqual(dll.pop_front(), model.pop(0))
            self.assertEqual(list(dll), model)
        check_links(self, dll)

    def test_unlink_and_errors(self) -> None:
        dll = DoublyLinkedList()
        a, b, c = dll.push_back("a"), dll.push_back("b"), dll.push_back("c")
        self.assertEqual(dll.unlink(b), "b")
        self.assertEqual(list(dll), ["a", "c"])
        check_links(self, dll)
        with self.assertRaises(ValueError):
            dll.unlink(dll._front)
        dll.unlink(a)
        dll.unlink(c)
        with self.assertRaises(IndexError):
            dll.pop_front()
        with self.assertRaises(IndexError):
            dll.pop_back()

    def test_music_player(self) -> None:
        p = ex.MusicPlayer(["A", "B", "C"])
        self.assertEqual([p.next(), p.next(), p.next(), p.previous()], ["B", "C", "C", "B"])
        self.assertEqual(p.remove_current(), "C")
        self.assertEqual(list(p.playlist), ["A", "C"])
        self.assertEqual(p.remove_current(), "A")
        self.assertEqual(p.remove_current(), None)
        self.assertIsNone(ex.MusicPlayer([]).now_playing())


class TestCircularAndPointers(unittest.TestCase):
    def test_round_robin(self) -> None:
        self.assertEqual(ex.round_robin(["Ana", "Ben", "Cy"], 7), ["Ana", "Ben", "Cy", "Ana", "Ben", "Cy", "Ana"])
        self.assertEqual(ex.round_robin([], 3), [])

    def test_middle(self) -> None:
        for n in range(1, 12):
            self.assertEqual(ex.middle(build(list(range(n)))).value, n // 2)  # type: ignore[union-attr]
        self.assertIsNone(ex.middle(None))

    def test_cycles(self) -> None:
        for n in range(1, 10):
            self.assertFalse(ex.has_cycle(build(list(range(n)))))
            self.assertEqual(sol.cycle_length(build(list(range(n)))), 0)
            for loop_to in range(n):
                head = make_cycle(list(range(n)), loop_to)
                self.assertTrue(ex.has_cycle(head))
                self.assertEqual(ex.cycle_start(head).value, loop_to)  # type: ignore[union-attr]
                self.assertEqual(sol.cycle_length(head), n - loop_to)

    def test_redirects(self) -> None:
        self.assertEqual(ex.redirect_loop({"/a": "/b", "/b": "/c", "/c": "/d", "/d": "/b"}, "/a"), "/b")
        self.assertIsNone(ex.redirect_loop({"/a": "/b", "/b": "/c"}, "/a"))


class TestSolutions(unittest.TestCase):
    def test_kth_and_palindrome(self) -> None:
        self.assertEqual(sol.kth_from_end(build([1, 2, 3, 4, 5]), 2).value, 4)  # type: ignore[union-attr]
        self.assertEqual(sol.kth_from_end(build([1, 2, 3]), 3).value, 1)        # type: ignore[union-attr]
        self.assertIsNone(sol.kth_from_end(build([1, 2]), 3))
        for values in ([], [1], [1, 2, 1], [1, 2, 2, 1], [1, 2], [1, 2, 3]):
            self.assertEqual(sol.is_palindrome_list(build(values)), values == values[::-1])

    def test_josephus(self) -> None:
        def brute(n: int, k: int) -> int:
            people, i = list(range(1, n + 1)), 0
            while len(people) > 1:
                i = (i + k - 1) % len(people)
                people.pop(i)
            return people[0]
        for n in range(1, 15):
            for k in range(1, 6):
                self.assertEqual(sol.josephus(n, k), brute(n, k))


if __name__ == "__main__":
    unittest.main()
