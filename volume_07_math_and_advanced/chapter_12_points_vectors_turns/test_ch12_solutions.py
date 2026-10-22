import itertools
import random
import unittest

import ch12_examples as ex
import ch12_solutions as sol


def brute(points) -> bool:
    return any(ex.cross(ex.sub(b, a), ex.sub(c, a)) == 0 for a, b, c in itertools.combinations(points, 3))


class TestThreeInALine(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertFalse(sol.three_in_a_line([]))
        self.assertFalse(sol.three_in_a_line([(1, 1)]))
        self.assertFalse(sol.three_in_a_line([(1, 1), (1, 1)]))
        self.assertTrue(sol.three_in_a_line([(1, 1), (1, 1), (5, 2)]))
        self.assertFalse(sol.three_in_a_line([(0, 0), (1, 0), (0, 1)]))

    def test_town(self) -> None:
        town = [(0, 0), (4, 1), (2, 5), (3, 5), (10, 4)]
        self.assertFalse(sol.three_in_a_line(town))
        self.assertTrue(sol.three_in_a_line(town + [(8, 2)]))     # (0, 0), (4, 1), (8, 2)
        self.assertTrue(sol.three_in_a_line([(0, 5), (0, -3), (0, 9)]))   # a vertical line

    def test_against_brute_force(self) -> None:
        r = random.Random(12)
        for _ in range(400):
            pts = [(r.randint(-4, 4), r.randint(-4, 4)) for _ in range(r.randint(0, 6))]
            self.assertEqual(sol.three_in_a_line(pts), brute(pts), pts)


if __name__ == "__main__":
    unittest.main()
