import random
import unittest

import ch23_examples as ex
import ch23_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_three_to_the_k(self) -> None:
        for k in range(1, 4):
            c = [0]
            x = int("1" * 2 ** k)
            self.assertEqual(ex.karatsuba(x, x, c), x * x)
            self.assertEqual(c[0], 3 ** k)

    def test_square(self) -> None:
        r = random.Random(23)
        for _ in range(200):
            x = r.randrange(0, 10 ** r.randint(1, 30))
            self.assertEqual(sol.karatsuba_square(x, [0]), x * x)
        with self.assertRaises(ValueError):
            sol.karatsuba_square(-1, [0])

    def test_crossover(self) -> None:
        self.assertEqual((sol.first_winning_size(1), sol.first_winning_size(32)), (512, 32))


if __name__ == "__main__":
    unittest.main()
