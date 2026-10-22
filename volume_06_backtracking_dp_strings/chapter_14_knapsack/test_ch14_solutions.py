import random
import unittest

import ch14_examples as ex
import ch14_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_one_row(self) -> None:
        r = random.Random(14)
        for _ in range(150):
            books = [(f"b{i}", r.randint(0, 9), r.randint(0, 9)) for i in range(r.randint(0, 7))]
            budget = r.randint(0, 25)
            self.assertEqual(ex.knapsack_one_row(books, budget), ex.knapsack(books, budget)[2][-1][budget])

    def test_limit(self) -> None:
        self.assertEqual([sol.best_with_limit(ex.BOOKS, 20, k) for k in range(5)], [0, 7, 13, 16, 16])
        r = random.Random(3)
        for _ in range(150):
            books = [(f"b{i}", r.randint(1, 9), r.randint(0, 9)) for i in range(r.randint(0, 7))]
            budget, k = r.randint(0, 25), r.randint(0, 4)
            self.assertEqual(sol.best_with_limit(books, budget, k), sol.brute_limit(books, budget, k))

    def test_free_book_refused(self) -> None:
        with self.assertRaises(ValueError):
            ex.unlimited([("free", 0, 5)], 3)


if __name__ == "__main__":
    unittest.main()
