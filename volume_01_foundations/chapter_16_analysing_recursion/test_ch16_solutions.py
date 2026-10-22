import random
import unittest

import ch16_solutions as sol


class TestMinMax(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        with self.assertRaises(ValueError):
            sol.shortest_and_tallest([])
        self.assertEqual(sol.shortest_and_tallest([150]), (150, 150, 0))
        self.assertEqual(sol.shortest_and_tallest([155, 142]), (142, 155, 1))
        self.assertEqual(sol.shortest_and_tallest([7, 7]), (7, 7, 1))

    def test_tallest_child_line(self) -> None:
        self.assertEqual(sol.shortest_and_tallest([142, 155, 138, 161, 150, 158]), (138, 161, 8))

    def test_power_of_two_formula(self) -> None:
        for k in range(1, 11):
            n = 2 ** k
            self.assertEqual(sol.shortest_and_tallest(list(range(n)))[2], 3 * n // 2 - 2)

    def test_against_builtins(self) -> None:
        rng = random.Random(16)
        for _ in range(300):
            xs = [rng.randint(100, 180) for _ in range(rng.randint(1, 40))]
            s, t, c = sol.shortest_and_tallest(xs)
            self.assertEqual((s, t), (min(xs), max(xs)))
            self.assertLessEqual(c, 2 * (len(xs) - 1))


if __name__ == "__main__":
    unittest.main()
