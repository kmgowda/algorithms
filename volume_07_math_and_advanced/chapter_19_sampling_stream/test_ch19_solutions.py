import itertools
import random
import unittest
from collections import Counter
from math import comb, factorial

import ch19_solutions as sol


class Feeder:
    def __init__(self, choices):
        self.choices = iter(choices)

    def randrange(self, m):
        return next(self.choices)


class TestSelectionSample(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.selection_sample([], 0, 0, random.Random(1)), [])
        self.assertEqual(sol.selection_sample("abc", 3, 0, random.Random(1)), [])
        self.assertEqual(sol.selection_sample("a", 1, 1, random.Random(1)), ["a"])
        self.assertEqual(sol.selection_sample("abc", 3, 3, random.Random(1)), list("abc"))
        with self.assertRaises(ValueError):
            sol.selection_sample("ab", 2, 3, random.Random(1))

    def test_every_run_is_fair(self) -> None:
        for n in range(1, 6):
            for k in range(n + 1):
                runs = Counter()
                for choices in itertools.product(*[range(n - s) for s in range(n)]):
                    runs[tuple(sol.selection_sample(range(n), n, k, Feeder(choices)))] += 1
                self.assertEqual(len(runs), comb(n, k))
                self.assertEqual(set(runs.values()), {factorial(n) // comb(n, k)})
                self.assertTrue(all(list(s) == sorted(s) for s in runs))      # stream order is kept


if __name__ == "__main__":
    unittest.main()
