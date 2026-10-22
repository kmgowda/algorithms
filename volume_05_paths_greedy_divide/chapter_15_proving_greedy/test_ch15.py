import unittest
from fractions import Fraction as F

import ch15_examples as ex


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

    def test_lateness(self) -> None:
        order = ex.earliest_deadline_first(ex.REPAIRS)
        self.assertEqual([j[0] for j in order], ["Atlas", "Novel", "Poems", "Comic", "Cookbook"])
        self.assertEqual(ex.lateness(order), (1, [("Atlas", 0, 3, 0), ("Novel", 3, 5, 0), ("Poems", 5, 6, 0),
                                                  ("Comic", 6, 10, 1), ("Cookbook", 10, 12, 0)]))
        self.assertEqual(ex.best_lateness(ex.REPAIRS), 1)
        self.assertEqual(ex.lateness(sorted(ex.REPAIRS, key=lambda j: j[1]))[0], 3)        # shortest job first
        r = ex.REPAIRS
        bad = [r[3], r[4], r[0], r[2], r[1]]
        steps = ex.remove_inversions(bad)
        self.assertEqual((ex.inversions(bad), len(steps) - 1, [l for _, l in steps]), (6, 6, [4, 4, 4, 2, 2, 1, 1]))
        self.assertEqual(ex.inversions(steps[-1][0]), 0)

    def test_lateness_practice(self) -> None:
        more = ex.REPAIRS + [("Map", 2, 4), ("Globe", 1, 12)]
        order = ex.earliest_deadline_first(more)
        self.assertEqual([j[0] for j in order], ["Map", "Atlas", "Novel", "Poems", "Comic", "Globe", "Cookbook"])
        self.assertEqual((ex.lateness(order)[0], ex.best_lateness(more)), (3, 3))
        r = ex.REPAIRS
        self.assertEqual(ex.inversions([r[4], r[3], r[2], r[1], r[0]]), 9)
        tied = [r[0], r[1], r[3], r[2], r[4]]
        self.assertEqual((ex.inversions(tied), ex.lateness(tied)[0]), (0, 1))
        two = [("Map", 3, 0), ("Globe", 1, 2)]
        edf = ex.earliest_deadline_first(two)
        self.assertEqual((ex.lateness(edf)[0], ex.total_lateness(edf)), (3, 5))
        self.assertEqual((ex.lateness(two[::-1])[0], ex.total_lateness(two[::-1])), (4, 4))

    def test_lateness_every_case(self) -> None:
        self.assertEqual((ex.lateness([]), ex.best_lateness([])), ((0, []), 0))
        self.assertEqual(ex.lateness([("A", 2, 5)]), (0, [("A", 0, 2, 0)]))
        trap = [("Map", 1, 2), ("Globe", 10, 10)]                                     # least slack first fails
        self.assertEqual(ex.lateness(sorted(trap, key=lambda j: j[2] - j[1]))[0], 9)
        self.assertEqual(ex.lateness(ex.earliest_deadline_first(trap))[0], 1)
        self.assertEqual(ex.lateness(ex.earliest_deadline_first([("A", 3, 1), ("B", 3, 1)]))[0], 5)
        import random
        rng = random.Random(14)
        for _ in range(100):
            jobs = [(str(i), rng.randint(1, 5), rng.randint(0, 15)) for i in range(rng.randint(0, 6))]
            self.assertEqual(ex.lateness(ex.earliest_deadline_first(jobs))[0], ex.best_lateness(jobs))

if __name__ == "__main__":
    unittest.main()
