import math
import random
import unittest
from collections import Counter

import ch04_examples as ex
import ch04_solutions as sol


class TestArraysHashing(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            nums = [rng.randint(-5, 15) for _ in range(rng.randint(0, 12))]
            present = set(nums)
            brute = max((L for x in present for L in range(1, 30) if all(x + i in present for i in range(L))), default=0)
            self.assertEqual(ex.longest_consecutive(nums), brute)
            if nums:
                self.assertEqual(ex.product_except_self(nums), [math.prod(nums[:i] + nums[i + 1:]) for i in range(len(nums))])
            s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 12)))
            subs = [s[i:j] for i in range(len(s)) for j in range(i, len(s) + 1)]
            self.assertEqual(ex.longest_unique_substring(s), max(len(x) for x in subs if len(set(x)) == len(x)))
            t = "".join(rng.choice("abc") for _ in range(rng.randint(1, 3)))
            covers = [x for x in subs if not Counter(t) - Counter(x)]
            got = ex.min_window(s, t)
            self.assertEqual(len(got), min((len(x) for x in covers), default=0))
            k = rng.randint(-5, 10)
            self.assertEqual(sol.subarray_sum_equals_k(nums, k),
                             sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if sum(nums[i:j]) == k))
            kk = rng.randint(0, 3)
            self.assertEqual(sol.character_replacement(s, kk),
                             max((len(x) for x in subs if len(x) - max(Counter(x).values(), default=0) <= kk), default=0))
            if len(nums) >= 3:
                self.assertEqual(ex.top_spender_session(nums, 3), max(sum(nums[i:i + 3]) for i in range(len(nums) - 2)))

    def test_examples(self) -> None:
        self.assertEqual(ex.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]),
                         [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]])
        self.assertEqual(ex.min_window("ADOBECODEBANC", "ABC"), "BANC")
        self.assertEqual(ex.top_spender_session([20, 5, 40, 10, 30, 5], 3), 80)
        board = [list("53..7...."), list("6..195..."), list(".98....6."), list("8...6...3"), list("4..8.3..1"),
                 list("7...2...6"), list(".6....28."), list("...419..5"), list("....8..79")]
        self.assertTrue(sol.is_valid_sudoku_rows(board))
        board[0][0] = "8"
        self.assertFalse(sol.is_valid_sudoku_rows(board))


if __name__ == "__main__":
    unittest.main()
