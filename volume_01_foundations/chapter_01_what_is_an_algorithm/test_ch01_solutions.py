import random
import unittest

import ch01_solutions as sol


class TestChapter1Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.shortest_and_tallest([147]), (147, 147, 0))
        self.assertEqual(sol.shortest_and_tallest([150, 162]), (150, 162, 1))
        self.assertEqual(sol.shortest_and_tallest([162, 150]), (150, 162, 1))
        self.assertEqual(sol.shortest_and_tallest([150, 150, 150]), (150, 150, 3))
        with self.assertRaises(IndexError):
            sol.shortest_and_tallest([])

    def test_chapter_line(self) -> None:
        self.assertEqual(sol.shortest_and_tallest(sol.HEIGHTS), (138, 161, 7))

    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            xs = [rng.randint(100, 200) for _ in range(rng.randint(1, 15))]
            shortest, tallest, comparisons = sol.shortest_and_tallest(xs)
            self.assertEqual((shortest, tallest), (min(xs), max(xs)))
            n = len(xs)
            self.assertEqual(comparisons, 3 * n // 2 - 2 if n % 2 == 0 else 3 * (n - 1) // 2)
            self.assertLessEqual(comparisons, 3 * n / 2)


if __name__ == "__main__":
    unittest.main()
