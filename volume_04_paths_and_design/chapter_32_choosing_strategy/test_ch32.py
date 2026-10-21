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


if __name__ == "__main__":
    unittest.main()
