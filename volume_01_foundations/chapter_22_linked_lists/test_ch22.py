import random
import unittest

import ch22_examples as ex


class TestChapter22(unittest.TestCase):
    def test_every_case(self) -> None:
        for v, ok, left in [(12, True, [25, 47, 63]), (47, True, [12, 25, 63]), (63, True, [12, 25, 47]),
                            (99, False, [12, 25, 47, 63])]:
            s = ex.LinkedList([12, 25, 47, 63])
            self.assertEqual((s.delete(v), s.values()), (ok, left))
        s = ex.LinkedList()
        self.assertFalse(s.delete(5))
        s = ex.LinkedList([7])
        self.assertEqual((s.delete(7), s.values()), (True, []))
        s = ex.LinkedList([47, 12, 47])
        s.delete(47)
        self.assertEqual(s.values(), [12, 47])
        s = ex.LinkedList()
        s.push_front(9)
        self.assertEqual(s.values(), [9])
        s = ex.LinkedList([12, 25])
        s.insert_after(s.find(25), 30)
        self.assertEqual(s.values(), [12, 25, 30])
        w = ex.WaitingList()
        for n in ("Ana", "Ben", "Cai"):
            w.join(n)
        w.cancel("Cai")
        w.join("Dev")
        self.assertEqual((w.names(), w.serve(), w.names()), (["Ana", "Ben", "Dev"], "Ana", ["Ben", "Dev"]))
        w.cancel("Dev")
        self.assertEqual((w.serve(), w.names()), ("Ben", []))
        with self.assertRaises(AttributeError):
            w.serve()

    def test_against_python_list(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            ref = [rng.randint(0, 9) for _ in range(rng.randint(0, 8))]
            ll = ex.LinkedList(ref)
            for _ in range(15):
                op, v = rng.choice(["front", "after", "delete"]), rng.randint(0, 9)
                if op == "front":
                    ll.push_front(v)
                    ref.insert(0, v)
                elif op == "after" and ref:
                    target = rng.choice(ref)
                    ll.insert_after(ll.find(target), v)
                    ref.insert(ref.index(target) + 1, v)
                elif op == "delete":
                    self.assertEqual(ll.delete(v), v in ref)
                    if v in ref:
                        ref.remove(v)
                self.assertEqual(ll.values(), ref)

    def test_doubly_every_case(self) -> None:
        d = ex.DoublyLinkedList()
        self.assertEqual((d.values(), d.values_backward(), d.size), ([], [], 0))
        self.assertIs(d.header.next, d.trailer)
        for pop in (d.pop_front, d.pop_back):
            with self.assertRaises(IndexError):
                pop()
        d.push_back(7)
        self.assertEqual((d.pop_back(), d.values(), d.size), (7, [], 0))
        self.assertIs(d.trailer.prev, d.header)
        d = ex.DoublyLinkedList([25, 47, 63])
        d.insert_between(58, d.find(47), d.find(63))
        self.assertEqual((d.values(), d.values_backward()), ([25, 47, 58, 63], [63, 58, 47, 25]))
        self.assertEqual(d.remove(d.find(47)), 47)
        self.assertEqual((d.values(), d.values_backward()), ([25, 58, 63], [63, 58, 25]))
        self.assertEqual((d.pop_front(), d.pop_back(), d.values(), d.size), (25, 63, [58], 1))
        self.assertIsNone(d.find(99))
        d.push_front(12)
        self.assertEqual(d.values(), [12, 58])

    def test_doubly_against_python_list(self) -> None:
        rng = random.Random(3)
        for _ in range(200):
            ref = [rng.randint(0, 9) for _ in range(rng.randint(0, 6))]
            d = ex.DoublyLinkedList(ref)
            for _ in range(20):
                op, v = rng.choice(["front", "back", "popf", "popb", "remove"]), rng.randint(0, 9)
                if op == "front":
                    d.push_front(v)
                    ref.insert(0, v)
                elif op == "back":
                    d.push_back(v)
                    ref.append(v)
                elif op == "popf" and ref:
                    self.assertEqual(d.pop_front(), ref.pop(0))
                elif op == "popb" and ref:
                    self.assertEqual(d.pop_back(), ref.pop())
                elif op == "remove" and v in ref:
                    d.remove(d.find(v))
                    ref.remove(v)
                self.assertEqual((d.values(), d.values_backward(), d.size), (ref, ref[::-1], len(ref)))

    def test_waiting_list(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            w, ref, k = ex.WaitingList(), [], 0
            for _ in range(20):
                op = rng.choice(["join", "join", "cancel", "serve"])
                if op == "join":
                    w.join(f"r{k}")
                    ref.append(f"r{k}")
                    k += 1
                elif op == "cancel" and ref:
                    name = rng.choice(ref)
                    w.cancel(name)
                    ref.remove(name)
                elif op == "serve" and ref:
                    self.assertEqual(w.serve(), ref.pop(0))
                self.assertEqual(w.names(), ref)


if __name__ == "__main__":
    unittest.main()
