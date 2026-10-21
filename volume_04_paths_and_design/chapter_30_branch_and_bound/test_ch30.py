import itertools
import unittest

import ch30_examples as ex


class TestChapter30(unittest.TestCase):
    def test_books(self) -> None:
        log = []
        self.assertEqual(ex.branch_and_bound(ex.BOOKS, 20, True, log), (16, ["Poems", "Atlas", "Novel"], 13))
        self.assertEqual(log[-1], (1, 0, 13.67, 16))
        self.assertEqual(ex.branch_and_bound(ex.BOOKS, 20, False)[2], 47)
        shop = ex.random_shop(20, 20)
        cap = sum(p for _, p, _ in shop) // 3
        self.assertEqual(ex.branch_and_bound(shop, cap)[::2], (69, 21))
        shop = ex.random_shop(30, 30)
        self.assertEqual(ex.branch_and_bound(shop, sum(p for _, p, _ in shop) // 3)[::2], (138, 128))

    def test_every_case(self) -> None:
        self.assertEqual((ex.branch_and_bound([], 20), ex.branch_and_bound(ex.BOOKS, 0)), ((0, [], 1), (0, [], 1)))
        self.assertEqual(ex.branch_and_bound(ex.BOOKS, 100)[0], 25)
        self.assertEqual(ex.branch_and_bound([("Big", 25, 9)], 20), (0, [], 2))
        items = sorted(ex.BOOKS, key=lambda b: b[2] / b[1], reverse=True)
        self.assertAlmostEqual(ex.fractional_bound(items, 1, 20), 13.6667, places=3)
        self.assertEqual(ex.fractional_bound(items, 4, 6), 2.0)
        shop = ex.random_shop(10, 10)
        cap = sum(p for _, p, _ in shop) // 3
        brute = max(sum(v for *_, v in c) for k in range(11) for c in itertools.combinations(shop, k)
                    if sum(p for _, p, _ in c) <= cap)
        self.assertEqual(ex.branch_and_bound(shop, cap)[0], brute)


if __name__ == "__main__":
    unittest.main()
