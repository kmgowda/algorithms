import itertools
import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestStateMachine(unittest.TestCase):
    def test_against_reference(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            p = [rng.randint(1, 20) for _ in range(rng.randint(0, 10))]
            self.assertEqual(ex.one_trade(p), sol.brute_trades(p, k=1))
            self.assertEqual(ex.unlimited_trades(p), sol.brute_trades(p))
            k = rng.randint(1, 3)
            self.assertEqual(ex.k_trades(p, k), sol.brute_trades(p, k=k))
            self.assertEqual(ex.with_cooldown(p), sol.brute_trades(p, cooldown=1))
            fee = rng.randint(0, 4)
            self.assertEqual(ex.with_fee(p, fee), sol.brute_trades(p, fee=fee))
            nums = [rng.randint(1, 9) for _ in range(rng.randint(0, 7))]
            best = max((sum(v if i % 2 == 0 else -v for i, v in enumerate(c))
                        for r in range(len(nums) + 1) for c in itertools.combinations(nums, r)), default=0)
            self.assertEqual(sol.max_alternating_sum(nums), best)
        for n in range(0, 7):
            for k in range(1, 4):
                count = sum(1 for c in itertools.product(range(k), repeat=n)
                            if all(not (c[i] == c[i + 1] == c[i + 2]) for i in range(n - 2)))
                self.assertEqual(sol.paint_fence(n, k), count if n else 0)

    def test_examples(self) -> None:
        self.assertEqual(ex.one_trade([7, 1, 5, 3, 6, 4]), 5)
        self.assertEqual(ex.unlimited_trades([7, 1, 5, 3, 6, 4]), 7)
        self.assertEqual(ex.k_trades([3, 3, 5, 0, 0, 3, 1, 4], 2), 6)
        self.assertEqual(ex.with_cooldown([1, 2, 3, 0, 2]), 3)
        self.assertEqual(ex.with_fee([1, 3, 2, 8, 4, 9], 2), 8)


if __name__ == "__main__":
    unittest.main()
