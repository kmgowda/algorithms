import itertools
import random
import unittest
from collections import Counter

import ch17_examples as ex


class FixedRng:
    """Feeds a fixed list of choices to a shuffle, to enumerate every possible run."""

    def __init__(self, choices):
        self.choices = iter(choices)

    def randrange(self, n):
        return next(self.choices)


class TestChapter17(unittest.TestCase):
    def test_examples(self) -> None:
        g = ex.LCG(42)
        self.assertEqual([g.below(100) for _ in range(8)], [27, 64, 53, 6, 35, 32, 33, 66])
        fy = ex.count_orders(ex.fisher_yates, 60000, 17)
        self.assertEqual((fy["abc"], fy["cba"]), (9907, 10133))
        nv = ex.count_orders(ex.naive_shuffle, 60000, 17)
        self.assertEqual((nv["abc"], nv["acb"]), (8851, 11202))
        t = ex.LCG(5, a=5, c=3, m=8)
        self.assertEqual([t.next() for _ in range(10)], [4, 7, 6, 1, 0, 3, 2, 5, 4, 7])

    def test_every_case(self) -> None:
        r = random.Random(1)
        self.assertEqual((ex.fisher_yates([], r), ex.fisher_yates([7], r)), ([], [7]))
        self.assertEqual(sorted(ex.fisher_yates(list(range(10)), r)), list(range(10)))
        # exact counts over every possible run: Fisher-Yates 6 runs, each order once; naive 27 runs, uneven
        fy = Counter("".join(ex.fisher_yates(list("abc"), FixedRng([j2, j1]))) for j2 in range(3) for j1 in range(2))
        nv = Counter("".join(ex.naive_shuffle(list("abc"), FixedRng(c))) for c in itertools.product(range(3), repeat=3))
        self.assertEqual(sorted(fy.values()), [1] * 6)
        self.assertEqual(sorted(nv.values()), [4, 4, 4, 5, 5, 5])


class TestDepth(unittest.TestCase):
    def test_exact_runs(self) -> None:
        for n in range(0, 6):
            runs = ex.all_fisher_yates_runs(n)
            self.assertEqual(sorted(runs.values()), [1] * len(list(itertools.permutations(range(n)))))
        self.assertEqual(sorted(set(ex.all_naive_runs(4).values())), [8, 9, 10, 11, 14, 15])
        import math
        self.assertEqual([n for n in range(2, 12) if n ** n % math.factorial(n) == 0], [2])

    def test_generators_and_bias(self) -> None:
        self.assertEqual((ex.full_period(5, 3, 8), ex.period(5, 3, 8, 5)), (True, 8))
        self.assertEqual((ex.full_period(4, 3, 8), ex.period(4, 3, 8, 5)), (False, 1))
        self.assertFalse(ex.full_period(5, 2, 8))
        for m in (8, 9, 10, 12, 16, 27):
            for a in range(m):
                for c in range(m):
                    self.assertEqual(ex.full_period(a, c, m), all(ex.period(a, c, m, s0) == m for s0 in range(m)))
        self.assertEqual((ex.modulo_bias(256, 10), ex.modulo_bias(256, 3)), ([26] * 6 + [25] * 4, [86, 85, 85]))
        r = random.Random(7)
        counts = Counter(ex.below_by_rejection(lambda: r.randrange(256), 10)[0] for _ in range(20000))
        self.assertTrue(all(1850 < counts[d] < 2150 for d in range(10)))
        self.assertEqual(ex.partial_shuffle(list(range(10)), 0, random.Random(1)), [])
        self.assertEqual(sorted(ex.partial_shuffle([5], 1, random.Random(1))), [5])


if __name__ == "__main__":
    unittest.main()
