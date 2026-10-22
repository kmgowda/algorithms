import random
import unittest

import ch23_solutions as sol


class TestChapter23Solutions(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(sol.search_rise_and_fall(sol.VISITORS, 50), 7)
        self.assertEqual(sol.search_rise_and_fall(sol.VISITORS, 66), 5)
        self.assertEqual(sol.search_rise_and_fall(sol.VISITORS, 45), 3)
        self.assertEqual(sol.search_rise_and_fall(sol.VISITORS, 40), -1)

    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.search_rise_and_fall([], 5), -1)
        self.assertEqual(sol.search_rise_and_fall([5], 5), 0)
        self.assertEqual(sol.search_rise_and_fall([5], 4), -1)
        self.assertEqual(sol.search_rise_and_fall([3, 9], 3), 0)
        self.assertEqual(sol.search_rise_and_fall([9, 3], 3), 1)
        self.assertEqual(sol.search_rise_and_fall([2, 7, 2], 2), 0)          # on both sides: the earlier one

    def test_against_brute_force(self) -> None:
        rng = random.Random(23)
        for _ in range(500):
            left = sorted(rng.sample(range(50), rng.randint(0, 8)))
            right = sorted(rng.sample(range(50), rng.randint(0, 8)), reverse=True)
            a = left + [99] + right
            for key in list(range(-1, 52)) + [99]:
                want = a.index(key) if key in a else -1
                self.assertEqual(sol.search_rise_and_fall(a, key), want)


if __name__ == "__main__":
    unittest.main()
