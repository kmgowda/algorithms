import math
import unittest

import ch15_examples as ex


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


    def test_moving_shelves(self) -> None:
        import itertools
        import random

        def brute(fl, k):
            rows, cols, n = len(fl), len(fl[0]), 0
            for downs in itertools.combinations(range(rows + cols - 2), rows - 1):
                r = c = 0
                pushed = fl[0][0]
                for i in range(rows + cols - 2):
                    if i in downs:
                        r += 1
                    else:
                        c += 1
                    pushed += fl[r][c]
                n += pushed <= k
            return n

        self.assertEqual([ex.count_paths_moving(ex.FLOOR, k) for k in range(3)], [(5, [5]), (22, [5, 17]), (35, [5, 17, 13])])
        self.assertEqual(ex.count_paths_moving([[1]], 0), (0, [0]))
        self.assertEqual(ex.count_paths_moving([[1]], 1), (1, [0, 1]))
        r = random.Random(7)
        for _ in range(100):
            fl = [[int(r.random() < 0.3) for _ in range(r.randint(1, 4))]]
            fl += [[int(r.random() < 0.3) for _ in fl[0]] for _ in range(r.randint(0, 3))]
            k = r.randint(0, 2)
            self.assertEqual(ex.count_paths_moving(fl, k)[0], brute(fl, k))
            self.assertEqual(ex.count_paths_moving(fl, 0)[0], ex.count_paths(fl)[0])


if __name__ == "__main__":
    unittest.main()
