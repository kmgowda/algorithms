import random
import unittest

import ch09_examples as ex


class TestChapter38(unittest.TestCase):
    def test_groups(self) -> None:
        self.assertEqual(ex.study_groups(ex.ROOM), [4, 3, 2, 3])
        self.assertEqual(ex.groups_with_diagonals(ex.ROOM), 4)
        self.assertEqual(ex.study_groups(["101", "010", "101"]), [1, 1, 1, 1, 1])
        rng = random.Random(1)
        for _ in range(200):
            g = ["".join(rng.choice("01") for _ in range(6)) for _ in range(5)]
            sizes = ex.study_groups(g)
            self.assertEqual(sum(sizes), sum(row.count("1") for row in g))

    def test_floor(self) -> None:
        d = ex.distances_from_exit(ex.FLOOR)
        self.assertEqual(max(d.values()), 16)
        self.assertEqual(ex.cut_off(ex.FLOOR), [(7, 8)])


if __name__ == "__main__":
    unittest.main()
