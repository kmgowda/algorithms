import random
import unittest

import ch19_examples as ex


class TestChapter19(unittest.TestCase):
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


    def test_knuth(self) -> None:
        self.assertEqual(ex.knuth_merge_cost(ex.STACKS), 36)
        table, tried, every = ex.knuth_trace(ex.STACKS)
        self.assertEqual((table[0], table[1][4], tried, every), ([None, 1, 1, 3, 3], 3, 15, 20))
        self.assertEqual([ex.knuth_merge_cost(s) for s in ([], [7], [3, 4], [2, 2, 2, 2], [9, 8, 8, 9, 4])], [0, 0, 7, 16, 89])
        r = random.Random(6)
        for _ in range(400):
            s = [r.randint(0, 9) for _ in range(r.randint(0, 12))]       # zeros make many ties
            self.assertEqual(ex.knuth_merge_cost(s), ex.merge_cost(s)[0])
        s = [r.randint(1, 50) for _ in range(200)]
        self.assertEqual(ex.knuth_merge_cost(s), ex.merge_cost(s)[0])
        self.assertLess(ex.knuth_trace(s)[1], 3 * 200 * 200)

    def test_matrix_chain(self) -> None:
        import random
        cost, table, split, brackets = ex.matrix_chain(ex.CHAIN)
        self.assertEqual((cost, brackets), (5000, "((A B) (C D))"))
        self.assertEqual([table[1][2], table[2][3], table[3][4], table[1][3], table[2][4]], [1500, 9000, 3000, 4500, 4500])
        self.assertEqual((split[1][3], split[2][4], split[1][4]), (2, 2, 2))
        self.assertEqual((ex.matrix_chain([10, 20])[0], ex.matrix_chain([10, 20])[3], ex.matrix_chain([])[0]), (0, "A", 0))
        self.assertEqual(ex.matrix_chain([2, 3, 4])[:1] + ex.matrix_chain([2, 3, 4])[3:], (24, "(A B)"))
        self.assertEqual((ex.matrix_chain([2, 3, 4, 1])[0], ex.matrix_chain([2, 3, 4, 1])[3]), (18, "(A (B C))"))
        r = random.Random(11)
        for _ in range(200):
            d = [r.randint(1, 30) for _ in range(r.randint(1, 8))]
            self.assertEqual(ex.matrix_chain(d)[0], ex.chain_brute(d))


if __name__ == "__main__":
    unittest.main()
