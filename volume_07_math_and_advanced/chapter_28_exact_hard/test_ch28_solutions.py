import itertools
import random
import unittest

import ch28_examples as ex
import ch28_solutions as sol


def brute_mis(vs, es):
    for k in range(len(vs), -1, -1):
        for g in itertools.combinations(vs, k):
            if not any(a in g and b in g for a, b in es):
                return k


class TestThinkingProblems(unittest.TestCase):
    def test_branching_calls(self) -> None:
        r = random.Random(28)
        for _ in range(100):
            vs = list(range(r.randint(1, 8)))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.4]
            k = r.randint(0, 5)
            calls = [0]
            ex.cover_branching(es, k, calls)
            self.assertLessEqual(calls[0], 2 ** (k + 1) - 1)

    def test_forest(self) -> None:
        got = sol.forest_independent_set(list("abcdefg"), [("a", "b"), ("b", "c"), ("c", "d"), ("b", "e"), ("f", "g")])
        self.assertEqual(len(got), 4)
        self.assertEqual(sol.forest_independent_set([], []), [])
        r = random.Random(3)
        for _ in range(150):
            n = r.randint(1, 9)
            vs = list(range(n))
            es = [(i, r.randrange(i)) for i in range(1, n) if r.random() < 0.8]     # a random forest
            chosen = sol.forest_independent_set(vs, es)
            self.assertFalse(any(a in chosen and b in chosen for a, b in es))
            self.assertEqual(len(chosen), brute_mis(vs, es))

    def test_unsorted_mitm(self) -> None:
        found, pairs = sol.mitm_unsorted(list(range(1, 17)), 10 ** 6)
        self.assertEqual((found, pairs), (False, 2 ** 16))
        self.assertEqual(ex.subset_sum_mitm(list(range(1, 17)), 10 ** 6), (False, 512))


if __name__ == "__main__":
    unittest.main()
