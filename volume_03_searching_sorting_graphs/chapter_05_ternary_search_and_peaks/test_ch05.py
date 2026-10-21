import random
import unittest

import ch05_examples as ex


class TestChapter05(unittest.TestCase):
    def test_always_a_peak(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            a = [rng.randint(0, 20) for _ in range(rng.randint(1, 30))]
            self.assertTrue(ex.is_peak(a, ex.peak_by_slope(a)))

    def test_unimodal_global(self) -> None:
        rng = random.Random(2)
        for _ in range(300):
            left = sorted(rng.sample(range(100), rng.randint(0, 10)))
            right = sorted(rng.sample(range(100), rng.randint(0, 10)), reverse=True)
            a = left + [200] + right
            self.assertTrue(ex.is_unimodal(a))
            self.assertEqual(a[ex.peak_by_slope(a)], 200)
        self.assertFalse(ex.is_unimodal([1, 3, 2, 5, 4]))

    def test_every_case(self) -> None:
        rows = [([3, 8, 15, 22, 30], 4, 2), ([30, 22, 15, 8, 3], 0, 3), ([4, 9, 15, 22, 27, 25, 18, 11], 4, 3),
                ([3, 7, 7, 7, 2], 1, 3), ([42], 0, 0), ([5, 5], 0, 1), ([6, 6, 6, 6], 0, 2), ([9, 4, 2, 6, 8], 4, 2)]
        for a, peak, comps in rows:
            t = []
            self.assertEqual(ex.peak_by_slope(a, t), peak)
            self.assertEqual(len(t), comps)
            self.assertTrue(ex.is_peak(a, peak))
        funcs = [(lambda h: h, 100, 8), (lambda h: -h, 0, 8), (ex.comfort, 46, 8),
                 (lambda h: min(h, 50) - max(0, h - 70), 50, 10)]
        for f, best, rounds in funcs:
            t = []
            self.assertEqual(ex.ternary_max(f, 0, 100, t), best)
            self.assertEqual(len(t), rounds)
        self.assertEqual(ex.ternary_max(ex.comfort, 40, 41), 41)

    def test_examples(self) -> None:
        t = []
        self.assertEqual(ex.peak_by_slope(ex.VISITORS, t), 5)
        self.assertEqual([x[2] for x in t], [5, 2, 4])
        self.assertEqual(ex.peak_by_slope(ex.BUMPY), 4)
        t = []
        self.assertEqual(ex.ternary_max(ex.comfort, 0, 100, t), 46)
        self.assertEqual(len(t), 8)
        for c in range(0, 60):
            f = lambda h, c=c: -(h - c) ** 2
            self.assertEqual(ex.ternary_max(f, 0, 100), c)


if __name__ == "__main__":
    unittest.main()
