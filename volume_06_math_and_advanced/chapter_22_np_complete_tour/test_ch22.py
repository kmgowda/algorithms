import unittest

import ch22_examples as ex


class TestChapter22(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(ex.satisfiable([[1, 2], [-1, 3], [-2, -3], [2, 3]], 3), ({1: False, 2: True, 3: False}, 3))
        self.assertEqual(ex.colouring(ex.TOWN, ex.ROADS, 2), (None, 256))
        c, tried = ex.colouring(ex.TOWN, ex.ROADS, 3)
        self.assertEqual((tried, all(c[a] != c[b] for a, b in ex.ROADS)), (1036, True))
        self.assertEqual((ex.vertex_cover(ex.TOWN, ex.ROADS, 3), ex.vertex_cover(ex.TOWN, ex.ROADS, 4)), (None, ["School", "Park", "Station", "Museum"]))
        self.assertEqual((ex.bin_packing([5, 4, 4, 3, 2, 2], 10, 2), ex.bin_packing([6, 6, 6], 10, 2)), ([0, 1, 1, 0, 0, 1], None))

    def test_every_case(self) -> None:
        self.assertEqual((ex.satisfiable([[1], [-1]], 1), ex.satisfiable([], 0)), ((None, 2), ({}, 1)))
        self.assertEqual((ex.colouring([], [], 1), ex.vertex_cover(["a", "b"], [], 0), ex.bin_packing([], 10, 1)), (({}, 1), [], []))
        self.assertIsNone(ex.bin_packing([11], 10, 3))


if __name__ == "__main__":
    unittest.main()
