import itertools
import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestFramework(unittest.TestCase):
    def test_against_brute(self) -> None:
        rng = random.Random(1)
        self.assertTrue(ex.random_check(300, rng))
        for _ in range(300):
            nums = [rng.randint(-8, 8) for _ in range(rng.randint(0, 9))]
            t = rng.randint(-12, 12)
            pairs = [(i, j) for i, j in itertools.combinations(range(len(nums)), 2) if nums[i] + nums[j] == t]
            self.assertEqual(sol.count_pairs(nums, t), len(pairs))
            self.assertEqual(sol.contains_duplicate(nums), len(set(nums)) < len(nums))
            s = sorted(nums)
            got = sol.two_sum_sorted(s, t)
            exists = any(s[i] + s[j] == t for i, j in itertools.combinations(range(len(s)), 2))
            self.assertEqual(got is not None, exists)
            if got:
                self.assertEqual(s[got[0]] + s[got[1]], t)

    def test_examples(self) -> None:
        self.assertEqual(ex.two_sum([2, 7, 11, 15], 9), [0, 1])
        self.assertEqual([ex.two_sum(n, t) for n, t in ex.edge_cases()], [[0, 1], [0, 1], [1, 3], [0, 3], None])
        self.assertEqual(ex.walkthrough([3, 2, 4], 6)[-1], "i=2, x=4: need 2, seen at 1 -> answer [1, 2]")
        self.assertEqual(len(ex.FRAMEWORK), 7)


if __name__ == "__main__":
    unittest.main()
