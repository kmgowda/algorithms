import itertools
import random
import unittest
from collections import Counter
from math import comb, factorial

import ch17_examples as ex
import ch17_solutions as sol


def every_run(n: int, k: int) -> Counter:
    ranges = [range(j + 1) for j in range(n - k, n)]
    return Counter(frozenset(sol.floyd_sample(n, k, ex.ChoiceFeeder(c))) for c in itertools.product(*ranges))


class TestFloydSample(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.floyd_sample(0, 0, random.Random(1)), set())
        self.assertEqual(sol.floyd_sample(5, 0, random.Random(1)), set())
        self.assertEqual(sol.floyd_sample(1, 1, random.Random(1)), {0})
        self.assertEqual(sol.floyd_sample(4, 4, random.Random(1)), {0, 1, 2, 3})
        with self.assertRaises(ValueError):
            sol.floyd_sample(3, 4, random.Random(1))

    def test_every_run_is_fair(self) -> None:
        for n in range(1, 7):
            for k in range(n + 1):
                runs = every_run(n, k)
                self.assertEqual(len(runs), comb(n, k))                       # every subset appears
                self.assertEqual(set(runs.values()), {factorial(k)})           # each from exactly k! runs

    def test_huge_population(self) -> None:
        s = sol.floyd_sample(10 ** 9, 3, random.Random(17))
        self.assertEqual(len(s), 3)
        self.assertTrue(all(0 <= x < 10 ** 9 for x in s))


if __name__ == "__main__":
    unittest.main()
