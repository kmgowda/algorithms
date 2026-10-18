import random
import unittest
from collections import deque

import ch12_examples as ex
import ch12_solutions as sol


class TestBoundedHistory(unittest.TestCase):
    def test_model(self) -> None:
        rng = random.Random(1)
        h, model = ex.BoundedHistory(4), []
        for i in range(500):
            h.add(str(i))
            model = (model + [str(i)])[-4:]
            h.check_invariants()
            k = rng.randint(0, 6)
            self.assertEqual(h.latest(k), model[-k:] if k else [])
            self.assertEqual(list(h), model)
        self.assertEqual(ex.show_latest(h, 2), " | ".join(model[-2:]))
        with self.assertRaises(ValueError):
            ex.BoundedHistory(0)
        with self.assertRaises(ValueError):
            h.latest(-1)


class TestGapBuffer(unittest.TestCase):
    def test_example(self) -> None:
        e = ex.GapBuffer("Hello zoo")
        e.move_cursor(6)
        e.insert("city ")
        self.assertEqual(str(e), "Hello city zoo")
        e.move_cursor(len(e))
        e.insert("!")
        e.delete_before(1)
        e.insert("!!")
        self.assertEqual(str(e), "Hello city zoo!!")

    def test_model(self) -> None:
        rng = random.Random(2)
        e, text, cursor = ex.GapBuffer("", gap=2), "", 0
        for _ in range(3000):
            op = rng.random()
            if op < 0.45:
                s = rng.choice(["a", "bc", "xyz", " "])
                e.insert(s)
                text = text[:cursor] + s + text[cursor:]
                cursor += len(s)
            elif op < 0.7:
                n = rng.randint(1, 3)
                e.delete_before(n)
                start = max(0, cursor - n)
                text = text[:start] + text[cursor:]
                cursor = start
            else:
                pos = rng.randint(-2, len(text) + 2)
                e.move_cursor(pos)
                cursor = max(0, min(pos, len(text)))
            e.check_invariants()
            self.assertEqual(str(e), text)
            self.assertEqual(e.cursor, cursor)
            self.assertEqual(len(e), len(text))


class TestMaxQueue(unittest.TestCase):
    def test_model(self) -> None:
        rng = random.Random(3)
        q, model = ex.MaxQueue(), deque()
        for _ in range(3000):
            if rng.random() < 0.55 or not model:
                v = rng.randint(0, 20)
                q.enqueue(v)
                model.append(v)
            else:
                self.assertEqual(q.dequeue(), model.popleft())
            if model:
                self.assertEqual(q.max(), max(model))
            self.assertEqual(len(q), len(model))
        empty = ex.MaxQueue()
        with self.assertRaises(IndexError):
            empty.dequeue()
        with self.assertRaises(IndexError):
            empty.max()


class TestSolutions(unittest.TestCase):
    def test_unique_queue(self) -> None:
        q = sol.UniqueQueue()
        self.assertEqual([q.enqueue(u) for u in ("/home", "/zoo", "/home")], [True, True, False])
        self.assertEqual(q.dequeue(), "/home")
        self.assertTrue(q.enqueue("/home"))
        q.check_invariants()
        self.assertEqual(len(q), 2)

    def test_playlist(self) -> None:
        p = sol.CircularPlaylist(["A", "B", "C"])
        self.assertEqual([p.next() for _ in range(4)], ["A", "B", "C", "A"])
        p.remove("C")
        self.assertEqual([p.next() for _ in range(3)], ["B", "A", "B"])
        p.remove("A")
        p.remove("B")
        with self.assertRaises(IndexError):
            p.next()

    def test_snapshot_counter(self) -> None:
        c = sol.SnapshotCounter()
        c.add(5)
        c.snapshot()
        c.add(10)
        c.rollback()
        self.assertEqual(c.value, 5)
        with self.assertRaises(IndexError):
            c.rollback()


if __name__ == "__main__":
    unittest.main()
