import random
import unittest
from collections import deque

import ch10_examples as ex
import ch10_solutions as sol


class TestRingBuffer(unittest.TestCase):
    def test_against_model(self) -> None:
        rng = random.Random(1)
        ring, model = ex.RingBuffer(5), deque()
        for _ in range(3000):
            if rng.random() < 0.55:
                v = rng.randint(0, 9)
                if len(model) == 5:
                    with self.assertRaises(OverflowError):
                        ring.enqueue(v)
                else:
                    ring.enqueue(v)
                    model.append(v)
            elif model:
                self.assertEqual(ring.dequeue(), model.popleft())
            self.assertEqual(list(ring), list(model))
        with self.assertRaises(ValueError):
            ex.RingBuffer(0)
        with self.assertRaises(IndexError):
            ex.RingBuffer(2).dequeue()

    def test_overwrite(self) -> None:
        self.assertEqual(ex.recent_readings([72, 75, 80, 78, 90, 85], 3), [78, 90, 85])
        self.assertEqual(ex.recent_readings([1, 2], 3), [1, 2])


class TestDeque(unittest.TestCase):
    def test_against_model(self) -> None:
        rng = random.Random(2)
        d, model = ex.Deque(), deque()
        for _ in range(4000):
            op = rng.random()
            v = rng.randint(0, 9)
            if op < 0.3:
                d.push_back(v)
                model.append(v)
            elif op < 0.6:
                d.push_front(v)
                model.appendleft(v)
            elif op < 0.8 and model:
                self.assertEqual(d.pop_front(), model.popleft())
            elif model:
                self.assertEqual(d.pop_back(), model.pop())
            self.assertEqual(list(d), list(model))
        empty = ex.Deque()
        with self.assertRaises(IndexError):
            empty.pop_front()
        with self.assertRaises(IndexError):
            empty.pop_back()

    def test_palindrome_and_stealing(self) -> None:
        self.assertTrue(ex.is_palindrome_deque("Never odd or even"))
        self.assertFalse(ex.is_palindrome_deque("zebra"))
        self.assertEqual(ex.work_stealing(["t1", "t2", "t3", "t4", "t5"]), (["t5", "t4", "t3"], ["t1", "t2"]))


class TestMonotonic(unittest.TestCase):
    def test_window_max_min(self) -> None:
        self.assertEqual(ex.sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7])
        rng = random.Random(3)
        for _ in range(300):
            values = [rng.randint(-10, 10) for _ in range(rng.randint(1, 15))]
            k = rng.randint(1, len(values))
            windows = [values[i:i + k] for i in range(len(values) - k + 1)]
            self.assertEqual(ex.sliding_window_max(values, k), [max(w) for w in windows])
            self.assertEqual(sol.sliding_window_min(values, k), [min(w) for w in windows])
        with self.assertRaises(ValueError):
            ex.sliding_window_max([1], 0)
        self.assertEqual(ex.peak_traffic_per_hour([12, 30, 18, 25, 40, 22, 15], 3), [30, 30, 40, 40, 40])


class TestSolutions(unittest.TestCase):
    def test_moving_average(self) -> None:
        self.assertEqual(sol.moving_average([10, 20, 30, 40], 3), [10.0, 15.0, 20.0, 30.0])

    def test_calm_stretch(self) -> None:
        self.assertEqual(sol.longest_calm_stretch([8, 2, 4, 7], 4), 2)
        self.assertEqual(sol.longest_calm_stretch([10, 1, 2, 4, 7, 2], 5), 4)
        rng = random.Random(4)
        for _ in range(200):
            r = [rng.randint(0, 10) for _ in range(rng.randint(1, 12))]
            limit = rng.randint(0, 6)
            brute = max(j - i + 1 for i in range(len(r)) for j in range(i, len(r))
                        if max(r[i:j + 1]) - min(r[i:j + 1]) <= limit)
            self.assertEqual(sol.longest_calm_stretch(r, limit), brute)

    def test_rotate(self) -> None:
        self.assertEqual(sol.rotate([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3])
        self.assertEqual(sol.rotate([1, 2, 3], -1), [2, 3, 1])


if __name__ == "__main__":
    unittest.main()
