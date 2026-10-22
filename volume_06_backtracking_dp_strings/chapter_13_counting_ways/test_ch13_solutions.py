import random
import unittest

import ch13_examples as ex
import ch13_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_invariant(self) -> None:
        for amount in range(0, 25):
            for j in range(len(ex.COINS) + 1):
                want = ex.brute_sets(amount, ex.COINS[:j]) if j else (1 if amount == 0 else 0)
                self.assertEqual(sol.sets_after(amount, ex.COINS, j)[amount], want)

    def test_distinct(self) -> None:
        self.assertEqual(sol.count_distinct(10, [2, 3, 5, 5, 7]), 4)
        r = random.Random(13)
        for _ in range(200):
            prices = [r.randint(1, 9) for _ in range(r.randint(0, 8))]
            a = r.randint(0, 20)
            self.assertEqual(sol.count_distinct(a, prices), sol.brute_distinct(a, prices))

    def test_zero_coin(self) -> None:
        with self.assertRaises(ValueError):
            ex.count_sets(3, [0, 1])
        with self.assertRaises(ValueError):
            ex.count_orders(3, [0, 1])


if __name__ == "__main__":
    unittest.main()
