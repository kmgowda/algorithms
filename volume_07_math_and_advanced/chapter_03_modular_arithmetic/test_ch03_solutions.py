import random
import unittest

import ch03_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.tower_mod(0, 0, 0, 7), 0)        # 0^(0^0) = 0^1 = 0
        self.assertEqual(sol.tower_mod(0, 0, 1, 7), 1)        # 0^(0^1) = 0^0 = 1
        self.assertEqual(sol.tower_mod(5, 0, 3, 7), 1)        # 5^0 = 1
        self.assertEqual(sol.tower_mod(3, 7, 0, 2), 1)        # modulus 2: odd numbers stay 1
        self.assertEqual(sol.tower_mod(4, 7, 5, 2), 0)

    def test_against_direct_power(self) -> None:
        rng = random.Random(3)
        for _ in range(400):
            p = rng.choice([2, 3, 5, 7, 11, 13, 101, 1_000_003])
            a, b, c = rng.randint(0, 50), rng.randint(0, 6), rng.randint(0, 4)
            self.assertEqual(sol.tower_mod(a, b, c, p), pow(a, b ** c, p))

    def test_weekday_and_huge(self) -> None:
        self.assertEqual(sol.tower_mod(10, 10, 2, 7), pow(10, 100, 7))
        self.assertEqual(sol.tower_mod(10, 10, 100, 7), 4)

    def test_wrong_shortcut(self) -> None:
        self.assertEqual((sol.power_reduced_exponent(2, 4, 12, 4), pow(2, 4, 12)), (1, 4))
        self.assertEqual(sol.power_reduced_exponent(5, 6, 12, 4), pow(5, 6, 12))   # coprime: fine


if __name__ == "__main__":
    unittest.main()
