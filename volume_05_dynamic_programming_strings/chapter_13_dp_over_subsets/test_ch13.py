import math
import random
import unittest

import ch13_examples as ex


class TestChapter13(unittest.TestCase):
    def test_round(self) -> None:
        d = ex.matrix(ex.BRANCHES, ex.TRAVEL)
        length, route, entries = ex.held_karp(d)
        self.assertEqual((length, [ex.BRANCHES[i] for i in route], entries), (21, ["Library", "East", "West", "South", "North", "Library"], 32))
        r = random.Random(13)
        pts = [(r.random(), r.random()) for _ in range(12)]
        dd = [[round(100 * math.dist(p, q)) for q in pts] for p in pts]
        self.assertEqual(ex.held_karp(dd)[::2], (291, 11264))

    def test_every_case(self) -> None:
        self.assertEqual((ex.held_karp([[0]])[0], ex.held_karp([[0, 4], [4, 0]])[:2], ex.held_karp([[0, 1, 2], [1, 0, 5], [2, 5, 0]])[0]),
                         (0, (8, [0, 1, 0]), 8))
        r = random.Random(1)
        for _ in range(30):
            n = r.randint(2, 7)
            d = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    d[i][j] = d[j][i] = r.randint(1, 20)
            length, route, _ = ex.held_karp(d)
            self.assertEqual(length, ex.brute(d))
            self.assertEqual(sum(d[a][b] for a, b in zip(route, route[1:])), length)
            self.assertEqual(sorted(route[1:-1]), list(range(1, n)))


if __name__ == "__main__":
    unittest.main()
