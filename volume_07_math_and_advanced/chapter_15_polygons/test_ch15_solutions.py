import random
import unittest

import ch15_examples as ex
import ch15_solutions as sol


def brute(poly) -> bool:
    """Strictly convex: distinct corners, and for every edge all other corners lie strictly on one common side."""
    n = len(poly)
    if n < 3 or len(set(poly)) < n:
        return False
    for sign in (1, -1):
        if all(sign * ex._cross(poly[i], poly[(i + 1) % n], q) > 0
               for i in range(n) for q in poly if q not in (poly[i], poly[(i + 1) % n])):
            return True
    return False


class TestIsConvex(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertFalse(sol.is_convex([]))
        self.assertFalse(sol.is_convex([(1, 1)]))
        self.assertFalse(sol.is_convex([(0, 0), (3, 1)]))
        self.assertTrue(sol.is_convex([(0, 0), (4, 0), (0, 3)]))
        self.assertTrue(sol.is_convex([(0, 0), (0, 3), (4, 0)]))            # clockwise
        self.assertFalse(sol.is_convex([(0, 0), (1, 1), (2, 2)]))           # flat

    def test_chapter_shapes(self) -> None:
        hexagon = [(4, 0), (8, 2), (8, 6), (4, 8), (0, 6), (0, 2)]
        self.assertEqual((sol.is_convex(ex.GARDEN), sol.is_convex(ex.STAR), sol.is_convex(hexagon)), (False, False, True))
        self.assertTrue(sol.is_convex(hexagon[::-1]))

    def test_against_brute_force(self) -> None:
        r = random.Random(15)
        for _ in range(3000):
            poly = [(r.randint(0, 6), r.randint(0, 6)) for _ in range(r.randint(0, 6))]
            self.assertEqual(sol.is_convex(poly), brute(poly), poly)


if __name__ == "__main__":
    unittest.main()
