import random
import unittest
from collections import Counter

import ch20_examples as ex
import ch20_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_exact_comparisons(self) -> None:
        for k in range(1, 11):
            n, c = 2 ** k, [0]
            vals = random.Random(k).sample(range(10 * n), n)
            self.assertEqual(ex.min_max(vals, c), (min(vals), max(vals)))
            self.assertEqual(c[0], 3 * n // 2 - 2)

    def test_majority(self) -> None:
        self.assertEqual((sol.majority([3, 1, 3, 3, 2, 3, 3]), sol.majority([1, 2, 3]), sol.majority([])), (3, None, None))
        r = random.Random(20)
        for _ in range(300):
            v = [r.choice("aab") for _ in range(r.randint(0, 12))]
            want = next((x for x, c in Counter(v).items() if 2 * c > len(v)), None)
            self.assertEqual(sol.majority(v), want)

    def test_empty_refused(self) -> None:
        with self.assertRaises(ValueError):
            ex.min_max([], [0])
        self.assertEqual(ex.min_max([7], [0]), (7, 7))


if __name__ == "__main__":
    unittest.main()
