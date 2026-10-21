import itertools
import unittest

import ch10_examples as ex


class TestChapter10(unittest.TestCase):
    def test_festival(self) -> None:
        log = []
        m = ex.max_matching(ex.CAN_DO, log)
        self.assertEqual(m, {"Tickets": "Ben", "Cafe": "Ana", "Stage": "Dev", "Signs": "Cai", "First aid": "Eva"})
        self.assertEqual(log[1][2], {"Tickets": "Ben", "Cafe": "Ana"})
        g = ex.greedy_matching(ex.CAN_DO)
        self.assertEqual((len(g), "Ben" in g.values()), (4, False))

    def test_assignment(self) -> None:
        self.assertEqual(ex.best_assignment(ex.MINUTES), (7, (0, 3, 1, 2)))
        self.assertEqual(ex.greedy_assignment(ex.MINUTES)[0], 17)

    def test_every_case(self) -> None:
        self.assertEqual((ex.max_matching({}), ex.max_matching({"A": []})), ({}, {}))
        self.assertEqual(ex.max_matching({"A": ["x"], "B": ["x"]}), {"x": "A"})
        self.assertEqual(ex.best_assignment([[5]]), (5, (0,)))
        two = {"Ana": ["Cafe", "Tickets"], "Ben": ["Cafe"]}
        self.assertEqual((len(ex.greedy_matching(two)), len(ex.max_matching(two))), (1, 2))
        # the matching is as large as any possible: brute force over all choices
        people = list(ex.CAN_DO)
        best = max(k for k in range(6) for group in itertools.combinations(people, k)
                   if any(len(set(c)) == k for c in itertools.product(*[ex.CAN_DO[p] for p in group])))
        self.assertEqual(best, 5)


if __name__ == "__main__":
    unittest.main()
