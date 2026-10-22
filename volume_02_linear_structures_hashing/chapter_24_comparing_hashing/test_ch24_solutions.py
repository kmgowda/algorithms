import random
import unittest

import ch24_solutions as sol

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


class TestRangeCounter(unittest.TestCase):
    def test_shelf(self) -> None:
        p = sol.range_counter(SHELF, 100)
        self.assertEqual([sol.count_between(p, a, b) for a, b in ((30, 60), (58, 58), (60, 30), (0, 99), (92, 99))],
                         [3, 1, 0, 9, 0])
        self.assertEqual(sol.count_between(p, -5, 500), 9)

    def test_smallest(self) -> None:
        self.assertEqual(sol.count_between(sol.range_counter([], 0), 0, 5), 0)
        self.assertEqual(sol.count_between(sol.range_counter([], 10), 0, 9), 0)
        self.assertEqual(sol.count_between(sol.range_counter([0], 1), 0, 0), 1)
        self.assertEqual(sol.count_between(sol.range_counter([3, 3, 3], 5), 0, 4), 1)

    def test_random(self) -> None:
        rng = random.Random(24)
        for _ in range(300):
            u = rng.randint(1, 40)
            keys = [rng.randrange(u) for _ in range(rng.randint(0, 20))]
            p = sol.range_counter(keys, u)
            a, b = rng.randint(-3, u + 3), rng.randint(-3, u + 3)
            self.assertEqual(sol.count_between(p, a, b), len({k for k in keys if a <= k <= b}))


if __name__ == "__main__":
    unittest.main()
