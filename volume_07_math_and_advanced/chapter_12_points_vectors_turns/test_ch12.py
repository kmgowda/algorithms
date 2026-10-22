import random
import unittest

import ch12_examples as ex


class TestChapter12(unittest.TestCase):
    def test_examples(self) -> None:
        u, v = ex.sub(ex.PARK, ex.LIBRARY), ex.sub(ex.MARKET, ex.LIBRARY)
        self.assertEqual((ex.dot(u, v), ex.cross(u, v), round(ex.angle_degrees(u, v), 1)), (13, 18, 54.2))
        self.assertEqual((ex.turn(ex.LIBRARY, ex.PARK, ex.MARKET), ex.turn(ex.LIBRARY, ex.MARKET, ex.PARK)), ("left", "right"))
        self.assertEqual((round(ex.distance(ex.LIBRARY, ex.MARKET), 3), ex.triangle_area(ex.LIBRARY, ex.PARK, ex.MARKET)), (5.385, 9.0))

    def test_every_case(self) -> None:
        self.assertEqual((ex.turn((0, 0), (0, 0), (1, 1)), ex.turn((0, 0), (1, 1), (3, 3)), ex.turn((0, 0), (2, 0), (1, 0))), ("straight",) * 3)
        self.assertLess(ex.dot((2, 0), (-1, 0)), 0)                     # the "straight" U-turn goes backwards
        self.assertEqual((ex.triangle_area((0, 0), (1, 1), (2, 2)), ex.dot((1, 0), (0, 1)), ex.angle_degrees((1, 0), (-1, 0))), (0.0, 0, 180.0))
        with self.assertRaises(ValueError):
            ex.angle_degrees((0, 0), (1, 0))
        r = random.Random(12)
        for _ in range(300):
            a, b, c = [(r.randint(-9, 9), r.randint(-9, 9)) for _ in range(3)]
            t1, t2 = ex.turn(a, b, c), ex.turn(c, b, a)
            self.assertEqual({t1, t2} == {"left", "right"} or t1 == t2 == "straight", True)


class TestDepth(unittest.TestCase):
    def test_projection_and_distances(self) -> None:
        foot, t = ex.projection((3, 5), (0, 2), (10, 4))
        self.assertAlmostEqual(t, 9 / 26)
        self.assertEqual(round(ex.distance_to_line((3, 5), (0, 2), (10, 4)), 3), 2.353)
        self.assertEqual((round(ex.distance_to_segment((12, 3), (0, 2), (10, 4)), 3), ex.distance_to_segment((1, 1), (0, 0), (0, 0))),
                         (2.236, 2 ** 0.5))
        self.assertEqual(ex.distance_to_segment((5, 7), (0, 0), (10, 0)), 7.0)
        with self.assertRaises(ValueError):
            ex.projection((1, 1), (2, 2), (2, 2))

    def test_robustness(self) -> None:
        tri = ((0.1, 0.3), (0.2, 0.6), (0.3, 0.9))
        self.assertEqual((ex.turn_sign(*tri), ex.turn_with_tolerance(*tri)), (1, "straight"))
        from fractions import Fraction as F
        self.assertEqual(ex.turn_sign(*[(F(str(x)), F(str(y))) for x, y in tri]), 0)
        a, b, c = (0.5 + 10 * 2 ** -53, 0.5), (12.0, 12.0), (24.0, 24.0)
        self.assertEqual([ex.turn_sign(a, b, c), ex.turn_sign(b, c, a), ex.turn_sign(c, a, b)], [-1, 0, -1])
        self.assertEqual([ex.exact_turn_sign(a, b, c), ex.exact_turn_sign(b, c, a), ex.exact_turn_sign(c, a, b)], [-1, -1, -1])


if __name__ == "__main__":
    unittest.main()
