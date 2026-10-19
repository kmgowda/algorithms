import itertools
import math
import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestCombinatorics(unittest.TestCase):
    def test_against_listing(self) -> None:
        for n in range(0, 8):
            for k in range(0, n + 1):
                self.assertEqual(ex.permutations_count(n, k), len(list(itertools.permutations(range(n), k))))
                self.assertEqual(ex.combinations_count(n, k), len(list(itertools.combinations(range(n), k))))
            balanced = sum(1 for s in itertools.product("()", repeat=2 * n)
                           if all(s[:i].count("(") >= s[:i].count(")") for i in range(2 * n + 1)) and s.count("(") == n)
            self.assertEqual(ex.catalan(n), balanced)
            for boxes in range(1, 4):
                self.assertEqual(ex.stars_and_bars(n, boxes), sum(1 for c in itertools.product(range(n + 1), repeat=boxes) if sum(c) == n))
        bm = ex.BinomialMod(2000)
        for n in range(0, 2000, 37):
            for k in range(0, n + 1, 11):
                self.assertEqual(bm.choose(n, k), math.comb(n, k) % ex.MOD)
        self.assertEqual(ex.pascal_rows(6)[-1], [1, 5, 10, 10, 5, 1])
        for w in ["AAB", "BANANA", "ABCD", "MISSIS"]:
            self.assertEqual(sol.anagram_count(w), len(set(itertools.permutations(w))))
        for n in range(1, 7):
            seats = {min(p[i:] + p[:i] for i in range(n)) for p in itertools.permutations(range(n))}
            self.assertEqual(sol.round_table(n), len(seats))

    def test_examples(self) -> None:
        self.assertEqual(ex.lottery_odds(49, 6), 13983816)
        self.assertEqual(ex.password_space(8, 62), 62 ** 8)
        self.assertEqual(sol.unique_paths(3, 7), 28)
        self.assertEqual(sol.num_trees(3), 5)


if __name__ == "__main__":
    unittest.main()
