import bisect
import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestBounds(unittest.TestCase):
    def test_against_bisect(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            items = sorted(rng.randint(0, 10) for _ in range(rng.randint(0, 12)))
            t = rng.randint(-1, 11)
            self.assertEqual(ex.lower_bound(items, t), bisect.bisect_left(items, t))
            self.assertEqual(ex.upper_bound(items, t), bisect.bisect_right(items, t))
            positions = [i for i, v in enumerate(items) if v == t]
            self.assertEqual(ex.find_range(items, t), (positions[0], positions[-1]) if positions else (-1, -1))
            a, b = sorted((rng.randint(0, 10), rng.randint(0, 10)))
            self.assertEqual(ex.count_between(items, a, b), sum(a <= v <= b for v in items))


class TestRotatedAndPeaks(unittest.TestCase):
    def test_rotated(self) -> None:
        rng = random.Random(2)
        for _ in range(300):
            base = sorted(rng.sample(range(50), rng.randint(1, 12)))
            r = rng.randrange(len(base))
            rot = base[r:] + base[:r]
            self.assertEqual(rot[ex.rotation_point(rot)], min(rot))
            t = rng.randint(-1, 51)
            self.assertEqual(ex.search_rotated(rot, t), rot.index(t) if t in rot else -1)

    def test_peak(self) -> None:
        rng = random.Random(3)
        for _ in range(300):
            h = rng.sample(range(100), rng.randint(1, 12))
            p = ex.find_peak(h)
            left = h[p - 1] if p > 0 else float("-inf")
            right = h[p + 1] if p + 1 < len(h) else float("-inf")
            self.assertTrue(h[p] > left and h[p] > right)

    def test_industry(self) -> None:
        limits, rates = [1, 5, 10], [50, 120, 200, 400]
        self.assertEqual([ex.shipping_rate(w, limits, rates) for w in (0.5, 1, 3.2, 10, 12)], [50, 50, 120, 200, 400])
        self.assertEqual(ex.logs_between([100, 105, 110, 110, 130, 150], 105, 130), (1, 5))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.insert_position([1, 3, 5, 6], 4), 2)
        self.assertEqual(sol.next_letter(["c", "f", "j"], "j"), "c")
        self.assertEqual(sol.next_letter(["c", "f", "j"], "a"), "c")
        self.assertEqual(sol.mountain_top([0, 2, 5, 3, 1]), 2)
        rng = random.Random(4)
        for _ in range(300):
            items = sorted(rng.randint(-10, 10) for _ in range(rng.randint(1, 10)))
            k = rng.randint(1, len(items))
            x = rng.randint(-12, 12)
            expected = sorted(sorted(items, key=lambda v: (abs(v - x), v))[:k])
            self.assertEqual(sol.k_closest(items, k, x), expected)
            pos = sorted(rng.sample(range(1, 30), rng.randint(0, 10)))
            kk = rng.randint(1, 10)
            missing = [v for v in range(1, 100) if v not in pos]
            self.assertEqual(sol.kth_missing(pos, kk), missing[kk - 1])


if __name__ == "__main__":
    unittest.main()
