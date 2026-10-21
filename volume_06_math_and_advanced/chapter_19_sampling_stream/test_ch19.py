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


if __name__ == "__main__":
    unittest.main()
