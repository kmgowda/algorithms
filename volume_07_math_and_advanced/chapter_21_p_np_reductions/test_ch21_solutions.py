import random
import unittest

import ch21_examples as ex
import ch21_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_reductions_compose(self) -> None:
        r = random.Random(21)
        for _ in range(60):
            prices = [r.randint(1, 15) for _ in range(r.randint(0, 7))]
            target = r.randint(0, 40)
            want = ex.find_subset(prices, target)[0] is not None
            once = sol.scale(prices, target, 3)
            twice = sol.scale(*once, 5)
            self.assertEqual(twice, sol.scale(prices, target, 15))
            self.assertEqual(ex.find_subset(*twice)[0] is not None, want)

    def test_find_with_oracle(self) -> None:
        chosen, calls = sol.find_with_oracle(ex.PRICES, 31)
        self.assertEqual((chosen, calls), ([4, 6, 7, 8], 11))
        self.assertTrue(ex.check_subset(ex.PRICES, chosen, 31))
        self.assertEqual(sol.find_with_oracle(ex.PRICES, 200), (None, 1))
        self.assertEqual(sol.find_with_oracle([], 0), ([], 1))
        r = random.Random(1)
        for _ in range(60):
            prices = [r.randint(1, 12) for _ in range(r.randint(0, 7))]
            target = r.randint(0, 30)
            chosen, calls = sol.find_with_oracle(prices, target)
            self.assertLessEqual(calls, len(prices) + 1)
            if chosen is None:
                self.assertIsNone(ex.find_subset(prices, target)[0])
            else:
                self.assertTrue(ex.check_subset(prices, chosen, target))


if __name__ == "__main__":
    unittest.main()
