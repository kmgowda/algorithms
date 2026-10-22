import math
import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestChapter6Solutions(unittest.TestCase):
    def test_match_jackets(self) -> None:
        self.assertEqual(sol.match_jackets([], []), [])
        self.assertEqual(sol.match_jackets([5], [5]), [(5, 5)])
        self.assertEqual(sol.match_jackets([2, 1], [1, 2]), [(1, 1), (2, 2)])
        with self.assertRaises(ValueError):
            sol.match_jackets([1, 2], [1, 3])
        rng = random.Random(7)
        for _ in range(200):
            n = rng.randint(0, 40)
            books = rng.sample(range(1000), n)
            jackets = list(books)
            rng.shuffle(jackets)
            pairs = sol.match_jackets(books, jackets, random.Random(rng.random()))
            self.assertEqual(pairs, [(b, b) for b in sorted(books)])

    def test_match_jackets_average(self) -> None:
        n, trials, total = 100, 300, 0
        for t in range(trials):
            rng = random.Random(t)
            books, jackets = list(range(n)), list(range(n))
            rng.shuffle(books)
            rng.shuffle(jackets)
            c = {"comparisons": 0}
            sol.match_jackets(books, jackets, random.Random(1000 + t), c)
            self.assertLessEqual(c["comparisons"], n * n)
            total += c["comparisons"]
        exact = 4 * (n + 1) * sum(1 / k for k in range(1, n + 1)) - 7 * n     # 2 x quicksort's average + n
        self.assertAlmostEqual(total / trials, exact, delta=0.03 * exact)
        self.assertAlmostEqual(exact, 2 * ex.closed_form(n) + n)
        self.assertLess(exact, 4 * n * math.log(n))

    def test_worst_inputs(self) -> None:
        self.assertEqual([len(sol.worst_inputs(n)) for n in range(1, 8)], [1, 2, 4, 8, 16, 32, 64])
        self.assertEqual(sol.worst_inputs(3), [(1, 2, 3), (2, 1, 3), (2, 3, 1), (3, 2, 1)])
        self.assertEqual(sol.worst_inputs(0), [()])

    def test_buggy_recursion(self) -> None:
        self.assertEqual(sol.buggy_quicksort_calls([12, 25], limit=5), [(0, 1)] * 5)
        self.assertEqual(sol.buggy_quicksort_calls([], limit=5), [(0, -1)])
        self.assertEqual(sol.buggy_quicksort_calls([7], limit=5), [(0, 0)])


if __name__ == "__main__":
    unittest.main()
