import itertools
import math
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestBacktrackingDP(unittest.TestCase):
    def test_backtracking(self) -> None:
        rng = random.Random(1)
        for n in range(0, 6):
            nums = list(range(n))
            self.assertEqual(sorted(ex.permutations(nums)), sorted(map(list, itertools.permutations(nums))))
            self.assertEqual(sorted(ex.subsets(nums)), sorted(list(c) for r in range(n + 1) for c in itertools.combinations(nums, r)))
            par = sol.generate_parentheses(n)
            self.assertEqual(len(par), math.comb(2 * n, n) // (n + 1))
        for _ in range(50):
            cands = sorted(set(rng.sample(range(2, 9), rng.randint(1, 4))))
            t = rng.randint(1, 15)
            got = sorted(map(tuple, ex.combination_sum(cands, t)))
            brute = sorted({tuple(sorted(c)) for r in range(1, t + 1) for c in itertools.combinations_with_replacement(cands, r) if sum(c) == t})
            self.assertEqual(got, brute)

    def test_dp(self) -> None:
        rng = random.Random(2)
        for _ in range(150):
            houses = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
            n = len(houses)
            self.assertEqual(ex.rob(houses), max(sum(houses[i] for i in range(n) if m >> i & 1) for m in range(1 << n) if m & m >> 1 == 0))
            coins = sorted(set(rng.sample(range(1, 8), rng.randint(1, 3))))
            amt = rng.randint(0, 15)
            fewest = min((r for r in range(amt + 1) for c in itertools.combinations_with_replacement(coins, r) if sum(c) == amt), default=-1)
            self.assertEqual(ex.coin_change(coins, amt), fewest)
            seq = [rng.randint(0, 9) for _ in range(rng.randint(0, 8))]
            lis = max((r for r in range(len(seq) + 1) for c in itertools.combinations(seq, r) if all(x < y for x, y in zip(c, c[1:]))), default=0)
            self.assertEqual(ex.length_of_lis(seq), lis)
            a = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))
            b = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))
            best = max((r for r in range(len(a) + 1) for c in itertools.combinations(a, r)
                        if (lambda it: all(ch in it for ch in c))(iter(b))), default=0)
            self.assertEqual(ex.lcs(a, b), best)
            self.assertEqual(sol.can_partition(houses), any(2 * sum(c) == sum(houses) for r in range(n + 1) for c in itertools.combinations(houses, r)))
        for n in range(10):
            self.assertEqual(ex.climb_stairs(n), [1, 1, 2, 3, 5, 8, 13, 21, 34, 55][n])
        self.assertEqual(sol.unique_paths(3, 7), 28)
        self.assertEqual(ex.fewest_bills(14), 2)


if __name__ == "__main__":
    unittest.main()
