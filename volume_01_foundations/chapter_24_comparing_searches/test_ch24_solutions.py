import random
import unittest

import ch24_solutions as sol


class TestKthOfTwo(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        with self.assertRaises(ValueError):
            sol.kth_of_two([], [], 1)
        with self.assertRaises(ValueError):
            sol.kth_of_two([12], [25], 0)
        self.assertEqual(sol.kth_of_two([12], [], 1), 12)
        self.assertEqual(sol.kth_of_two([], [25], 1), 25)
        self.assertEqual(sol.kth_of_two([25], [12], 1), 12)
        self.assertEqual(sol.kth_of_two([25], [12], 2), 25)

    def test_maya_shelves(self) -> None:
        a, b = [12, 31, 58, 70, 91], [25, 47, 63, 84]
        self.assertEqual([sol.kth_of_two(a, b, k) for k in range(1, 10)], [12, 25, 31, 47, 58, 63, 70, 84, 91])

    def test_against_merge(self) -> None:
        rng = random.Random(24)
        for _ in range(500):
            a = sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 8)))
            b = sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 8)))
            both = sorted(a + b)
            for k in range(1, len(both) + 1):
                self.assertEqual(sol.kth_of_two(a, b, k), both[k - 1])


if __name__ == "__main__":
    unittest.main()
