import unittest
from fractions import Fraction as F

import ch14_examples as ex


class TestChapter14(unittest.TestCase):
    def test_budget(self) -> None:
        votes, taken = ex.fractional(ex.BOOKS, 20)
        self.assertEqual((votes, taken), (F(49, 3), [("Poems", 1), ("Cookbook", 1), ("Atlas", F(5, 9))]))
        plan = {"Atlas": F(1), "Novel": F(1), "Poems": F(1), "Comic": F(0), "Cookbook": F(0)}
        self.assertEqual(ex.exchange_gain(ex.BOOKS, plan, 20), [("Atlas", "Cookbook", 9, F(3, 10)), ("Novel", "Cookbook", 6, F(1, 5))])
        self.assertLessEqual(ex.best_fraction_check(ex.BOOKS, 20), F(49, 3))
        best_plan = {"Poems": F(1), "Cookbook": F(1), "Atlas": F(5, 9), "Novel": F(0), "Comic": F(0)}
        self.assertEqual(ex.exchange_gain(ex.BOOKS, best_plan, 20), [])

    def test_exercises(self) -> None:
        self.assertEqual(ex.fractional(ex.BOOKS, 15)[0], 13)
        plan = {"Comic": F(1), "Cookbook": F(1), "Poems": F(1), "Atlas": F(0), "Novel": F(0)}
        self.assertEqual([g for *_, g in ex.exchange_gain(ex.BOOKS, plan, 20)], [F(4, 3), F(4, 3)])

    def test_every_case(self) -> None:
        self.assertEqual((ex.fractional(ex.BOOKS, 0)[0], ex.fractional([], 20)[0], ex.fractional(ex.BOOKS, 100)[0]), (0, 0, 25))
        self.assertEqual(ex.fractional(ex.BOOKS, 3), (F(18, 5), [("Poems", F(3, 5))]))
        self.assertEqual(ex.fractional([("A", 4, 4), ("B", 2, 2)], 3), (3, [("A", F(3, 4))]))


if __name__ == "__main__":
    unittest.main()
