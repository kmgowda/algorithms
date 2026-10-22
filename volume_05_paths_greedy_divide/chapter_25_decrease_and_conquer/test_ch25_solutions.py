import math
import unittest

import ch25_examples as ex
import ch25_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_multiplication_count(self) -> None:
        for n in range(1, 2000):
            c = [0]
            self.assertEqual(ex.power(3, n, c), 3 ** n)
            self.assertEqual(c[0], sol.multiplications(n))

    def test_isqrt(self) -> None:
        for n in list(range(300)) + [10 ** 12, 10 ** 12 - 1, 2 ** 61]:
            r, steps = sol.isqrt_halving(n)
            self.assertEqual(r, math.isqrt(n))
            self.assertLessEqual(steps, (n + 1).bit_length())
        self.assertEqual(sol.isqrt_halving(10 ** 12), (10 ** 6, 40))
        with self.assertRaises(ValueError):
            sol.isqrt_halving(-1)

    def test_negative_power(self) -> None:
        with self.assertRaises(ValueError):
            ex.power(2, -1, [0])
        self.assertEqual(ex.power(2, 0, [0]), 1)


if __name__ == "__main__":
    unittest.main()
