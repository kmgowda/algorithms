import random
import unittest

import ch22_examples as ex
import ch22_solutions as sol


def brute_extra(grid):
    best = max(ex.study_groups(grid), default=0) if grid else 0
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "0":
                g = [list(x) for x in grid]
                g[r][c] = "1"
                best = max(best, max(ex.study_groups(["".join(x) for x in g])))
    return best


class TestBestExtraSeat(unittest.TestCase):
    def test_smallest(self) -> None:
        self.assertEqual(sol.best_extra_seat([]), (0, None))
        self.assertEqual(sol.best_extra_seat(["0"]), (1, (0, 0)))
        self.assertEqual(sol.best_extra_seat(["1"]), (1, None))

    def test_room(self) -> None:
        self.assertEqual(sol.best_extra_seat(ex.ROOM), (8, (1, 2)))
        self.assertEqual(sol.best_extra_seat(["010", "101", "010"]), (5, (1, 1)))

    def test_random(self) -> None:
        rng = random.Random(22)
        for _ in range(300):
            g = ["".join(rng.choice("01") for _ in range(rng.randint(1, 5))) for _ in range(1)]
            w = len(g[0])
            g += ["".join(rng.choice("01") for _ in range(w)) for _ in range(rng.randint(0, 4))]
            self.assertEqual(sol.best_extra_seat(g)[0], brute_extra(g))


class TestCornerCount(unittest.TestCase):
    def test_counterexample(self) -> None:
        self.assertEqual(sol.count_by_corners(["101", "111"]), 2)
        self.assertEqual(len(ex.study_groups(["101", "111"])), 1)
        self.assertEqual(sol.count_by_corners(ex.ROOM), len(ex.study_groups(ex.ROOM)))


if __name__ == "__main__":
    unittest.main()
