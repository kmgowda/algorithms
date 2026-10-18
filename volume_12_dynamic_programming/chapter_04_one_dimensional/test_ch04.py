import itertools
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


class TestOneDimensional(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            v = [rng.randint(0, 20) for _ in range(rng.randint(1, 10))]
            n = len(v)
            brute = max(sum(v[i] for i in range(n) if m >> i & 1) for m in range(1 << n) if m & (m >> 1) == 0)
            self.assertEqual(ex.house_robber(v), brute)
            circ = max(sum(v[i] for i in range(n) if m >> i & 1) for m in range(1 << n)
                       if m & (m >> 1) == 0 and not (n > 1 and m & 1 and m >> (n - 1) & 1))
            self.assertEqual(ex.house_robber_circle(v), circ)
            seq = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
            brute_lis = max((r for r in range(len(seq) + 1) for c in itertools.combinations(seq, r)
                             if all(a < b for a, b in zip(c, c[1:]))), default=0)
            self.assertEqual(ex.lis_quadratic(seq), brute_lis)
            self.assertEqual(ex.lis_fast(seq), brute_lis)
            got = sol.lis_sequence(seq)
            self.assertEqual(len(got), brute_lis)
            self.assertTrue(all(a < b for a, b in zip(got, got[1:])))
            coins = sorted(set(rng.sample(range(1, 9), rng.randint(1, 3))))
            amount = rng.randint(0, 20)
            combos = [c for r in range(amount + 1) for c in itertools.combinations_with_replacement(coins, r) if sum(c) == amount]
            self.assertEqual(ex.coin_change_ways(coins, amount), len(combos))
            self.assertEqual(ex.coin_change_min(coins, amount), min((len(c) for c in combos), default=-1))

    def test_examples(self) -> None:
        self.assertEqual(ex.climb_stairs(10), 89)
        self.assertEqual(ex.climb_stairs(10, (1, 2, 3)), 274)
        self.assertEqual(ex.house_robber([2, 7, 9, 3, 1]), 12)
        self.assertEqual(ex.coin_change_min([2], 3), -1)
        self.assertEqual(ex.longest_growth_streak([120, 90, 150, 140, 160, 130, 170, 200, 180]), 5)
        self.assertEqual(sol.max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
        self.assertEqual(sol.decode_count("226"), 3)
        self.assertEqual(sol.decode_count("06"), 0)
        self.assertEqual(sol.perfect_squares(12), 3)
        self.assertEqual(sol.perfect_squares(13), 2)


if __name__ == "__main__":
    unittest.main()
