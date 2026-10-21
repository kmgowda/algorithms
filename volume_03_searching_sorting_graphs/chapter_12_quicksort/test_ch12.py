import random
import sys
import unittest

import ch12_examples as ex


class TestChapter12(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
