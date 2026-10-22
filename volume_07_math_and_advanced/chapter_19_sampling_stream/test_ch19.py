import itertools
import random
import unittest
from collections import Counter
from fractions import Fraction

import ch19_examples as ex


class Fixed:
    def __init__(self, choices):
        self.c = iter(choices)

    def randrange(self, n):
        return next(self.c)


class TestChapter19(unittest.TestCase):
    def test_examples(self) -> None:
        rng = random.Random(19)
        counts = Counter()
        for _ in range(30000):
            counts.update(ex.reservoir(range(10), 3, rng))
        self.assertEqual((counts[0], counts[2], sum(counts.values())), (8894, 9132, 90000))
        self.assertEqual((ex.reservoir(range(2), 5, rng), ex.reservoir([], 3, rng), ex.reservoir(range(100), 0, rng)), ([0, 1], [], []))
        w = Counter(ex.weighted_pick(["a", "b", "c"], [1, 2, 7], rng) for _ in range(10000))
        self.assertEqual((w["a"], w["b"], w["c"]), (975, 2052, 6973))

    def test_every_case(self) -> None:
        # exact: over every possible run, each of 5 items is kept in exactly 2/5 of runs for k = 2
        runs = list(itertools.product(range(3), range(4), range(5)))
        kept = Counter()
        for c in runs:
            kept.update(ex.reservoir(range(5), 2, Fixed(c)))
        self.assertEqual({Fraction(v, len(runs)) for v in kept.values()}, {Fraction(2, 5)})
        with self.assertRaises(ValueError):
            ex.reservoir([1], -1, random.Random(1))
        with self.assertRaises(ValueError):
            ex.weighted_pick(["a"], [-1], random.Random(1))
        self.assertIsNone(ex.weighted_pick([], [], random.Random(1)))
        self.assertEqual(ex.weighted_pick(["a", "b"], [0, 5], random.Random(1)), "b")


class TestDepth(unittest.TestCase):
    def test_exact_inclusion(self) -> None:
        from fractions import Fraction
        for n in range(1, 7):
            for k in range(0, n + 1):
                self.assertEqual(ex.exact_inclusion(n, k), [Fraction(min(k, n), n)] * n)

    def test_merge(self) -> None:
        import math
        from fractions import Fraction
        self.assertEqual(ex.merge_count_distribution(2, 2, 2), [Fraction(1, 6), Fraction(2, 3), Fraction(1, 6)])
        self.assertEqual(ex.merge_count_distribution(2, 2, 2, biased=True), [Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)])
        for n1 in range(1, 6):
            for n2 in range(1, 6):
                for k in range(0, min(n1, n2) + 1):
                    expect = [Fraction(math.comb(n1, j) * math.comb(n2, k - j), math.comb(n1 + n2, k)) for j in range(k + 1)]
                    self.assertEqual(ex.merge_count_distribution(n1, n2, k), expect)
        r = random.Random(20)
        counts = Counter()
        for _ in range(30000):
            a = ex.reservoir(range(0, 4), 2, r)
            b = ex.reservoir(range(4, 8), 2, r)
            counts.update(ex.merge_reservoirs(a, 4, b, 4, 2, r))
        self.assertTrue(all(7100 < counts[x] < 7900 for x in range(8)))      # each item 2/8 of 30,000 = 7,500

    def test_weighted_and_skipping(self) -> None:
        r = random.Random(21)
        self.assertEqual((ex.weighted_sample([], [], 3, r), ex.weighted_sample(["a"], [5], 0, r), ex.weighted_sample(["a", "b"], [0, 1], 2, r)),
                         ([], [], ["b"]))
        firsts = Counter(ex.weighted_sample(["a", "b"], [1, 3], 1, r)[0] for _ in range(20000))
        self.assertAlmostEqual(firsts["b"] / 20000, 0.75, delta=0.02)
        sample, used = ex.reservoir_skipping(range(1_000_000), 100, random.Random(5))
        self.assertEqual((len(sample), len(set(sample)), used), (100, 100, 2696))
        self.assertEqual(ex.reservoir_skipping(range(3), 5, r), ([0, 1, 2], 0))
        counts = Counter()
        rr = random.Random(22)
        for _ in range(20000):
            counts.update(ex.reservoir_skipping(range(10), 3, rr)[0])
        self.assertTrue(all(5600 < counts[x] < 6400 for x in range(10)))


if __name__ == "__main__":
    unittest.main()
