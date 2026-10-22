import random
import unittest

import ch13_examples as ex
import ch13_solutions as sol


def brute(horizontals, verticals) -> int:
    return sum(ex.segments_cross((x1, y), (x2, y), (x, y1), (x, y2))
               for y, x1, x2 in horizontals for x, y1, y2 in verticals)


class TestGridCrossings(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.count_grid_crossings([], []), 0)
        self.assertEqual(sol.count_grid_crossings([(0, 0, 5)], []), 0)
        self.assertEqual(sol.count_grid_crossings([], [(0, 0, 5)]), 0)
        self.assertEqual(sol.count_grid_crossings([(2, 0, 4)], [(2, 0, 4)]), 1)
        self.assertEqual(sol.count_grid_crossings([(2, 0, 4)], [(4, 2, 9)]), 1)     # touching ends count
        self.assertEqual(sol.count_grid_crossings([(2, 0, 4)], [(5, 0, 9)]), 0)

    def test_town_grid(self) -> None:
        streets = [(1, 0, 6), (3, 2, 8), (5, 0, 4)]
        avenues = [(1, 0, 5), (3, 2, 6), (7, 0, 2)]
        self.assertEqual(sol.count_grid_crossings(streets, avenues), brute(streets, avenues))
        self.assertEqual(sol.count_grid_crossings(streets, avenues), 4)

    def test_against_brute_force(self) -> None:
        r = random.Random(13)
        for _ in range(300):
            hs = [(r.randint(0, 6), *sorted((r.randint(0, 6), r.randint(0, 6)))) for _ in range(r.randint(0, 5))]
            vs = [(r.randint(0, 6), *sorted((r.randint(0, 6), r.randint(0, 6)))) for _ in range(r.randint(0, 5))]
            self.assertEqual(sol.count_grid_crossings(hs, vs), brute(hs, vs), (hs, vs))


if __name__ == "__main__":
    unittest.main()
