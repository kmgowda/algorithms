import random
import unittest

import ch13_examples as ex


class TestChapter13(unittest.TestCase):
    def test_paths(self) -> None:
        self.assertEqual(ex.crossing_pairs(ex.PATHS), [("A", "B"), ("A", "D")])

    def test_every_case(self) -> None:
        got = [ex.segments_cross(*s) for s in (((0, 0), (4, 0), (2, 0), (6, 0)), ((0, 0), (2, 0), (3, 0), (5, 0)),
                                                ((0, 0), (2, 2), (2, 2), (4, 0)), ((0, 0), (2, 2), (3, 3), (5, 5)), ((1, 1), (1, 1), (0, 0), (2, 2)))]
        self.assertEqual(got, [True, False, True, False, True])
        self.assertEqual((ex.segments_cross((1, 1), (7, 3), (0, 4), (6, 0)), ex.segments_cross((1, 1), (7, 3), (0, 0), (6, 4)),
                          ex.segments_cross((0, 4), (6, 0), (2, 0), (4, 0))), (True, True, False))
        r = random.Random(13)
        for _ in range(300):
            s = [(r.randint(0, 4), r.randint(0, 4)) for _ in range(4)]
            self.assertEqual(ex.segments_cross(*s), ex.segments_cross(s[2], s[3], s[0], s[1]))


if __name__ == "__main__":
    unittest.main()
