import math
import unittest

import ch07_examples as ex


class TestChapter7(unittest.TestCase):
    def test_floor(self) -> None:
        n, table = ex.count_paths(ex.FLOOR)
        self.assertEqual((n, table[2]), (5, [1, 1, 2, 2, 3]))
        self.assertEqual(ex.count_paths([[0] * 5 for _ in range(4)])[0], math.comb(7, 3))
        total, least, route = ex.cheapest(ex.DUST)
        self.assertEqual((total, route), (11, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (3, 3)]))
        self.assertEqual(sum(ex.DUST[r][c] for r, c in route), 11)

    def test_every_case(self) -> None:
        self.assertEqual([ex.count_paths(f)[0] for f in ([[0]], [[1]], [[0, 1], [1, 0]], [[0, 0, 0]])], [1, 0, 0, 1])
        self.assertEqual((ex.cheapest([[5]])[0], ex.cheapest([[1, 2, 3]])[0]), (5, 6))
        self.assertEqual(ex.count_paths([[0] * 10 for _ in range(10)])[0], 48620)
        f = [r[:] for r in ex.FLOOR]
        f[2][3] = 1
        self.assertEqual((ex.count_paths(f)[0], ex.count_paths([[0] * 3 for _ in range(3)])[0], ex.cheapest(ex.DUST)[1][3][0]), (1, 6, 13))


if __name__ == "__main__":
    unittest.main()
