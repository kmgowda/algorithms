import random
import unittest

import ch11_examples as ex


class TestChapter11(unittest.TestCase):
    def test_stacks(self) -> None:
        cost, table, plan = ex.merge_cost(ex.STACKS)
        self.assertEqual((cost, plan, table[0]), (36, "((4 + (1 + 3)) + (6 + 2))", [0, 5, 12, 26, 36]))
        self.assertEqual(ex.merge_cost([9, 8, 8, 9, 4])[::2], (89, "((9 + 8) + (8 + (9 + 4)))"))
        self.assertEqual(ex.greedy_smallest_pair([9, 8, 8, 9, 4]), 92)

    def test_every_case(self) -> None:
        self.assertEqual([ex.merge_cost(s)[0] for s in ([], [7], [3, 4], [2, 2, 2, 2])], [0, 0, 7, 16])
        r = random.Random(11)
        for _ in range(200):
            s = [r.randint(1, 9) for _ in range(r.randint(1, 6))]
            self.assertEqual(ex.merge_cost(s)[0], ex.brute(s))


if __name__ == "__main__":
    unittest.main()
