import unittest

import ch32_examples as ex


class TestChapter32(unittest.TestCase):
    def test_budget(self) -> None:
        self.assertEqual(ex.budget_table(), {"brute force": (16, 32), "greedy (votes per pound)": (15, 1),
                                             "backtracking": (16, 61), "branch and bound": (16, 13)})

    def test_every_case(self) -> None:
        got = []
        for n in (10, 20, 25):
            c = [0]
            got.append((ex.ways_naive(n, c), c[0], ex.ways_remembered(n)))
        self.assertEqual(got, [(89, 177, (89, 11)), (10946, 21891, (10946, 21)), (121393, 242785, (121393, 26))])
        c = [0]
        self.assertEqual((ex.ways_naive(0, c), c[0], ex.ways_remembered(0), ex.ways_remembered(2)), (1, 1, (1, 1), (2, 3)))
        self.assertEqual((len(ex.coins.greedy_change(6, ex.coins.ODD)), len(ex.coins.fewest_coins(6, ex.coins.ODD))), (3, 2))


    def test_change_four_ways(self) -> None:
        self.assertEqual(ex.change_comparison(30, [25, 10, 1]),
                         {"greedy": (6, 3), "plain recursion": (3, 570), "backtracking with a bound": (3, 66),
                          "table": (3, 31)})
        self.assertEqual(ex.change_comparison(6, [4, 3, 1]),
                         {"greedy": (3, 3), "plain recursion": (2, 24), "backtracking with a bound": (2, 17),
                          "table": (2, 7)})
        self.assertEqual(ex.change_plain(40, [25, 10, 1]), (4, 3558))
        inf = float("inf")
        self.assertEqual([v[0] for v in ex.change_comparison(3, [5, 2]).values()], [inf] * 4)
        self.assertEqual([v[0] for v in ex.change_comparison(0, [4, 3, 1]).values()], [0] * 4)
        for a in range(25):
            self.assertEqual(ex.change_backtracking(a, [7, 5, 1])[0], ex.change_table(a, [7, 5, 1])[0])


if __name__ == "__main__":
    unittest.main()
