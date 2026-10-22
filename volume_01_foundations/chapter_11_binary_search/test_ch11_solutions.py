import random
import unittest

import ch11_solutions as sol


def brute(a: list[int]) -> int:
    return next((i for i, v in enumerate(a) if v == i), -1)


class TestChapter11Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.matching_slot([]), -1)
        self.assertEqual(sol.matching_slot([0]), 0)
        self.assertEqual(sol.matching_slot([5]), -1)
        self.assertEqual(sol.matching_slot([-3]), -1)
        self.assertEqual(sol.matching_slot([0, 1]), 0)
        self.assertEqual(sol.matching_slot([-1, 1]), 1)

    def test_example(self) -> None:
        self.assertEqual(sol.matching_slot(sol.CASE), 3)
        self.assertEqual(sol.matching_slot([12, 25, 31, 47, 58, 63, 70, 84, 91]), -1)

    def test_against_brute_force(self) -> None:
        rng = random.Random(11)
        for _ in range(1000):
            n = rng.randint(0, 12)
            a = sorted(rng.sample(range(-8, 20), n))
            self.assertEqual(sol.matching_slot(a), brute(a))


if __name__ == "__main__":
    unittest.main()
