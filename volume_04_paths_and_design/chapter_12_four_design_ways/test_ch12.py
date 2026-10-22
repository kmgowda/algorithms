import unittest

import ch12_examples as ex


class TestChapter12(unittest.TestCase):
    def test_budget(self) -> None:
        self.assertEqual(ex.brute_force(ex.BOOKS, ex.BUDGET), (16, ("Atlas", "Novel", "Poems"), 32))
        self.assertEqual(ex.greedy(ex.BOOKS, ex.BUDGET, key=lambda b: -b[2]), (13, ("Cookbook", "Atlas")))
        self.assertEqual(ex.greedy(ex.BOOKS, ex.BUDGET, key=lambda b: b[1]), (12, ("Poems", "Comic", "Novel")))
        self.assertEqual(ex.greedy(ex.BOOKS, ex.BUDGET, key=lambda b: -b[2] / b[1]), (15, ("Poems", "Cookbook", "Comic")))
        self.assertEqual(ex.divide_and_conquer_max([v for *_, v in ex.BOOKS]), 7)
        self.assertEqual(ex.backtracking(ex.BOOKS, ex.BUDGET), (16, ("Atlas", "Novel", "Poems"), 61))

    def test_every_case(self) -> None:
        self.assertEqual((ex.brute_force([], 20), ex.backtracking([], 20)), ((0, (), 1), (0, (), 1)))
        self.assertEqual(ex.brute_force(ex.BOOKS, 0)[:2], (0, ()))
        self.assertEqual(ex.brute_force(ex.BOOKS, 100)[0], 25)
        self.assertEqual(ex.backtracking(ex.BOOKS, 100)[2], 63)
        self.assertEqual(ex.brute_force([("Big", 25, 9)], 20)[:2], (0, ()))
        self.assertEqual(ex.divide_and_conquer_max([4]), 4)
        self.assertEqual(ex.brute_force(ex.BOOKS, 25)[0], 19)
        self.assertEqual(ex.greedy(ex.BOOKS, 25, key=lambda b: -b[2] / b[1])[0], 19)

    def test_counting_branches(self) -> None:
        self.assertEqual(ex.backtracking(ex.BOOKS, ex.BUDGET, check_first=True), (16, ("Atlas", "Novel", "Poems"), 51))
        self.assertEqual(ex.backtracking(ex.BOOKS, 0), (0, (), 11))
        self.assertEqual(ex.backtracking([], 0, check_first=True), (0, (), 1))

if __name__ == "__main__":
    unittest.main()
