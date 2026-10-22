import math
import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_register_adds_mod_256(self) -> None:
        for a in range(-300, 300, 7):
            for b in range(-300, 300, 11):
                self.assertEqual(ex.wrap(a + b), ex.wrap(ex.wrap(a) + ex.wrap(b)))
                self.assertEqual((ex.wrap(a + b) - (a + b)) % 256, 0)

    def test_pairwise(self) -> None:
        big = [1e16] + [1.0] * 10000
        self.assertEqual((sol.pairwise_sum(big) - 1e16, sum(big) - 1e16), (10000.0, 0.0))
        self.assertEqual((sol.pairwise_sum([]), sol.pairwise_sum([2.5])), (0.0, 2.5))
        r = random.Random(11)
        v = [r.uniform(0, 1) for _ in range(100000)]
        exact = math.fsum(v)
        self.assertLessEqual(abs(sol.pairwise_sum(v) - exact), abs(ex.naive_sum(v) - exact) + 1e-12)

    def test_tenths(self) -> None:
        self.assertEqual(sol.tenths_until_one(), (False, 1000))
        self.assertEqual(sol.tenths_fixed(), 10)
        self.assertNotEqual(ex.add_tenths(10), 1.0)


if __name__ == "__main__":
    unittest.main()
