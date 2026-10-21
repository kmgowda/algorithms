import math
import random
import unittest

import ch20_examples as ex


class TestChapter20(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.inversions_brute(ex.RANKS), ex.sort_count(ex.RANKS)[1]), (9, 9))
        d, pair = ex.closest_pair(ex.BOXES)
        self.assertEqual((round(d, 3), pair), (1.414, ((2, 3), (3, 4))))

    def test_every_case(self) -> None:
        self.assertEqual([ex.sort_count(a)[1] for a in ([], [1, 2, 3], [3, 2, 1], [2, 2, 1], list(range(8, 0, -1)))], [0, 0, 3, 2, 28])
        self.assertEqual(ex.closest_pair([(0, 0), (3, 4)])[0], 5.0)
        self.assertEqual([ex.sort_count(a)[1] for a in ([1, 2, 3, 4, 5, 6, 8, 7], [4, 3, 2, 1], [2, 7, 3, 5])], [1, 6, 2])
        self.assertEqual(ex.closest_pair([(1, 1), (1, 1), (5, 5)])[0], 0.0)
        r = random.Random(1)
        for _ in range(300):
            p = [(r.randint(0, 50), r.randint(0, 50)) for _ in range(r.randint(2, 25))]
            self.assertTrue(math.isclose(ex.closest_pair(p)[0], ex.closest_brute(p)[0]))
            a = [r.randint(0, 9) for _ in range(r.randint(0, 20))]
            self.assertEqual(ex.sort_count(a)[1], ex.inversions_brute(a))


if __name__ == "__main__":
    unittest.main()
