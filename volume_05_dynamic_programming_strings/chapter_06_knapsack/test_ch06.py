import random
import unittest

import ch06_examples as ex


class TestChapter6(unittest.TestCase):
    def test_budget(self) -> None:
        votes, names, table = ex.knapsack(ex.BOOKS, 20)
        self.assertEqual((votes, names), (16, ["Atlas", "Novel", "Poems"]))
        self.assertEqual([r[20] for r in table], [0, 6, 10, 16, 16, 16])
        self.assertEqual((ex.knapsack_one_row(ex.BOOKS, 20), ex.unlimited(ex.BOOKS, 20)), (16, 24))
        self.assertEqual([ex.knapsack(ex.BOOKS, b)[0] for b in range(0, 41, 5)], [0, 6, 8, 13, 16, 19, 23, 25, 25])

    def test_every_case(self) -> None:
        self.assertEqual([ex.knapsack(b, m)[:2] for b, m in (([], 20), (ex.BOOKS, 0), ([("Big", 25, 9)], 20))], [(0, [])] * 3)
        self.assertEqual(ex.knapsack(ex.BOOKS, 100)[0], 25)
        self.assertEqual((ex.unlimited([("Poems", 5, 6)], 20), ex.unlimited(ex.BOOKS, 4)), (24, 0))
        self.assertEqual((ex.knapsack(ex.BOOKS, 10)[:2], ex.knapsack(ex.BOOKS, 16)[0], ex.knapsack(ex.BOOKS + [("Poster", 4, 3)], 20)[0]), ((8, ["Poems", "Comic"]), 13, 16))
        r = random.Random(6)
        for _ in range(100):
            books = [(str(i), r.randint(1, 12), r.randint(1, 9)) for i in range(r.randint(0, 8))]
            m = r.randint(0, 30)
            self.assertEqual(ex.knapsack(books, m)[0], ex.brute(books, m))
            self.assertEqual(ex.knapsack_one_row(books, m), ex.brute(books, m))


    def test_subset_sums(self) -> None:
        reach = ex.subset_sums([p for _, p, _ in ex.BOOKS], 35)
        self.assertEqual([t for t in range(36) if not reach[t]], [1, 2, 3, 4, 7, 8, 12, 13, 17, 18, 22, 23, 27, 28, 31, 32, 33, 34])
        self.assertEqual((ex.subset_sums([], 3), ex.subset_sums([5], 0)), ([True, False, False, False], [True]))
        self.assertEqual((ex.unlimited([("Poems", 5, 6)], 15), ex.knapsack_one_row([("Poems", 5, 6)], 15)), (18, 6))


if __name__ == "__main__":
    unittest.main()
