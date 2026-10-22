import math
import unittest

import ch30_examples as ex


class TestChapter30(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual([ex.largest_input(r, 10 ** 8) for r in ex.GROWTH], [100000000, 4523071, 10000, 464, 26, 11])
        self.assertEqual(ex.advise("sub-problems repeat"), [("dynamic programming", "Volume 6, Part II")])
        self.assertEqual(ex.advise("routes on a map")[0][1], "Volume 5, Part I")
        self.assertEqual(ex.fastest_fitting(50_000, 10 ** 8), ["n", "n log n"])

    def test_plans(self) -> None:
        self.assertTrue(ex.hard_problem_plan(20, 10 ** 8).startswith("exact: try"))
        self.assertEqual(ex.hard_problem_plan(40, 10 ** 8), "exact: meet in the middle")
        self.assertEqual(ex.hard_problem_plan(1000, 10 ** 8, small_parameter=10), "exact: fixed-parameter search")
        self.assertEqual(ex.hard_problem_plan(1000, 10 ** 8), "approximation with a proven ratio")
        self.assertEqual(ex.hard_problem_plan(1000, 10 ** 8, need_proof_of_quality=False), "local search")
        self.assertEqual(ex.big_data_plan(False, True, 1, True), "streaming sketch")
        self.assertEqual(ex.big_data_plan(False, False, 50, True), "MapReduce")
        self.assertEqual(ex.big_data_plan(True, True, 1, True), "ordinary in-memory algorithm")

    def test_branch_sites(self) -> None:
        self.assertEqual(math.comb(40, 5), 658008)
        self.assertEqual(ex.exact_steps(40, 5, 10_000), 32_900_400_000)
        s, h = ex.town()
        g = ex.greedy_sites(s, h, 3)
        l = ex.swap_search(g, s, h)
        e = ex.exact_sites(s, h, 3)
        rg, rl, re = (ex.radius(c, s, h) for c in (g, l, e))
        self.assertEqual((round(rg, 2), round(rl, 2), round(re, 2)), (6.73, 5.3, 5.05))
        self.assertLessEqual(re, rl)
        self.assertLessEqual(rl, rg)
        self.assertLessEqual(rg, 3 * re)

    def test_greedy_guarantee_many_towns(self) -> None:
        for seed in range(15):
            s, h = ex.town(10, 60, seed)
            for k in (1, 2, 3):
                self.assertLessEqual(ex.radius(ex.greedy_sites(s, h, k), s, h), 3 * ex.radius(ex.exact_sites(s, h, k), s, h) + 1e-9)

    def test_every_case(self) -> None:
        self.assertEqual((ex.largest_input("n", 0), ex.largest_input("n", 1), ex.largest_input("2^n", 1)), (0, 1, 0))
        self.assertEqual((ex.advise(""), ex.advise("banana")), ([], []))
        for rate, f in ex.GROWTH.items():
            n = ex.largest_input(rate, 10 ** 6)
            self.assertLessEqual(f(n), 10 ** 6)
            self.assertGreater(f(n + 1), 10 ** 6)
        s, h = ex.town(5, 20, 1)
        self.assertEqual(ex.radius(ex.greedy_sites(s, h, 5), s, h), ex.radius(ex.exact_sites(s, h, 5), s, h))


if __name__ == "__main__":
    unittest.main()
