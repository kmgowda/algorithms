import random
import unittest

import ch02_solutions as sol


class TestChapter2Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.add_binary("", ""), "0")
        self.assertEqual(sol.add_binary("0", ""), "0")
        self.assertEqual(sol.add_binary("0", "0"), "0")
        self.assertEqual(sol.add_binary("1", "0"), "1")
        self.assertEqual(sol.add_binary("1", "1"), "10")
        self.assertEqual(sol.add_binary("0001", "1"), "10")

    def test_worked_examples(self) -> None:
        self.assertEqual(sol.add_binary("1001101", "11001"), "1100110")   # 77 + 25 = 102
        self.assertEqual(sol.add_binary("11111111", "1"), "100000000")    # 255 + 1 = 256

    def test_against_brute_force(self) -> None:
        rng = random.Random(2)
        for _ in range(1000):
            a, b = rng.randint(0, 5000), rng.randint(0, 5000)
            self.assertEqual(sol.add_binary(bin(a)[2:], bin(b)[2:]), bin(a + b)[2:])


if __name__ == "__main__":
    unittest.main()
