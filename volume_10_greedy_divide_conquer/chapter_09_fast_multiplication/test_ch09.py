import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestFastMultiplication(unittest.TestCase):
    def test_numbers(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            x, y = rng.randrange(10 ** rng.randint(1, 60)), rng.randrange(10 ** rng.randint(1, 60))
            dx, dy = ex.to_digits(x), ex.to_digits(y)
            self.assertEqual(ex.from_digits(ex.schoolbook(dx, dy)), x * y)
            self.assertEqual(ex.from_digits(ex.karatsuba(dx, dy, cutoff=2)), x * y)
            self.assertEqual(sol.karatsuba_int(x, y), x * y)

    def test_matrices(self) -> None:
        rng = random.Random(2)
        for n in (1, 2, 4, 8, 16):
            A = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
            B = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
            self.assertEqual(ex.strassen(A, B, cutoff=1), ex.mat_mult(A, B))

    def test_race_and_solutions(self) -> None:
        r = ex.race_multiplication(1600)
        self.assertLess(r["karatsuba"], r["schoolbook"])
        self.assertEqual(sol.multiplications_needed(1024, "four"), 1024 ** 2)
        self.assertEqual(sol.multiplications_needed(1024, "three"), 3 ** 10)
        a, b, c, d = 1, 2, 3, 4
        self.assertEqual(sol.complex_multiply_three(a, b, c, d), (a * c - b * d, a * d + b * c))
        self.assertAlmostEqual(sol.exponent(3, 2), 1.585, places=3)


if __name__ == "__main__":
    unittest.main()
