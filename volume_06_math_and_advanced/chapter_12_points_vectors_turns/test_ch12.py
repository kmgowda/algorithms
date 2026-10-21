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


if __name__ == "__main__":
    unittest.main()
