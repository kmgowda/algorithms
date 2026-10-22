import random
import unittest

import ch27_examples as ex
import ch27_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_comparisons(self) -> None:
        for n in range(1, 300):
            c = [0]
            vals = list(range(n))
            self.assertEqual(ex.max_dc(vals, c), n - 1)
            self.assertEqual(c[0], n - 1)

    def test_where(self) -> None:
        self.assertEqual(sol.best_stretch_where([-2, 5, -1, 4, -7, 3]), (8, 1, 3))
        self.assertEqual(sol.best_stretch_where([-4, -1, -3]), (-1, 1, 1))
        r = random.Random(27)
        for _ in range(200):
            v = [r.randint(-9, 9) for _ in range(r.randint(1, 12))]
            total, a, b = sol.best_stretch_where(v)
            self.assertEqual(total, sum(v[a:b + 1]))
            self.assertEqual(total, max(sum(v[i:j + 1]) for i in range(len(v)) for j in range(i, len(v))))
            self.assertEqual(total, ex.stretch_greedy(v))

    def test_empty(self) -> None:
        with self.assertRaises(ValueError):
            ex.max_dc([], [0])


if __name__ == "__main__":
    unittest.main()
