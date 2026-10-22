import random
import sys
import unittest

import ch06_examples as ex


PILE9 = [58, 25, 91, 12, 70, 47, 84, 31, 63]
CASES = [PILE9, sorted(PILE9), sorted(PILE9, reverse=True), [47] * 9, [58, 25, 58, 12, 25, 47, 58, 12, 47], [47], []]


class TestChapter12(unittest.TestCase):
    def test_every_case(self) -> None:
        got = []
        for a in CASES:
            c = {"comparisons": 0}
            b = list(a)
            ex.quicksort(b, counter=c)
            self.assertEqual(b, sorted(a))
            got.append(c["comparisons"])
        self.assertEqual(got, [17, 36, 36, 36, 17, 0, 0])

    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 30) for _ in range(rng.randint(0, 40))]
            b = list(a)
            ex.quicksort(b)
            self.assertEqual(b, sorted(a))

    def test_examples(self) -> None:
        a, c, log = list(ex.PILE), {"comparisons": 0}, []
        ex.quicksort(a, counter=c, log=log)
        self.assertEqual((c["comparisons"], c["max_depth"]), (17, 3))
        self.assertEqual(log[0], (0, 63, [58, 25, 12, 47, 31], [84, 70, 91]))
        b = [40, 10, 50, 20, 30]
        self.assertEqual(ex.partition(b, 0, 4), 2)

    def test_sorted_is_quadratic(self) -> None:
        sys.setrecursionlimit(10_000)
        _, comps, depth = ex.measure(list(range(500)))
        self.assertEqual((comps, depth), (500 * 499 // 2, 499))

    def test_average_case(self) -> None:
        self.assertEqual(ex.expected_comparisons(0), 0)
        self.assertEqual(ex.expected_comparisons(1), 0)
        self.assertAlmostEqual(ex.expected_comparisons(2), 1.0)
        self.assertAlmostEqual(ex.expected_comparisons(3), 8 / 3)
        for n in (2, 3, 9, 50, 200):
            self.assertAlmostEqual(ex.expected_comparisons(n), ex.closed_form(n), places=6)
        self.assertAlmostEqual(ex.expected_comparisons(9), 20.579, places=3)
        self.assertAlmostEqual(ex.pair_probability(2, 6), 0.4)
        self.assertAlmostEqual(ex.average_random_pivot(PILE9, 20000), 20.58, delta=0.1)
        b = [5, 3, 5, 1]
        self.assertEqual(ex.random_pivot_comparisons(b, random.Random(1)) >= 0, True)
        self.assertEqual(b, [1, 3, 5, 5])
        self.assertEqual(ex.random_pivot_comparisons([], random.Random(1)), 0)


if __name__ == "__main__":
    unittest.main()
