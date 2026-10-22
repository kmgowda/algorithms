import random
import unittest
from functools import reduce

import ch01_examples as ex
import ch01_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.gcd_without_each([]), [])
        self.assertEqual(sol.gcd_without_each([7]), [0])
        self.assertEqual(sol.gcd_without_each([0, 5]), [5, 0])

    def test_donations(self) -> None:
        self.assertEqual(sol.gcd_without_each([84, 36, 60, 90]), [6, 6, 6, 12])

    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            vals = [rng.randint(0, 200) for _ in range(rng.randint(1, 8))]
            want = [reduce(ex.gcd, vals[:i] + vals[i + 1:], 0) for i in range(len(vals))]
            self.assertEqual(sol.gcd_without_each(vals), want)

    def test_product_rule_fails_for_three(self) -> None:
        self.assertEqual(sol.lcm_by_product([12, 18]), ex.lcm_many([12, 18]))
        self.assertEqual((sol.lcm_by_product([2, 4, 8]), ex.lcm_many([2, 4, 8])), (32, 8))

    def test_mersenne(self) -> None:
        for m in range(1, 30):
            for n in range(1, 30):
                self.assertEqual(sol.mersenne_gcd(m, n), 2 ** ex.gcd(m, n) - 1)


if __name__ == "__main__":
    unittest.main()
