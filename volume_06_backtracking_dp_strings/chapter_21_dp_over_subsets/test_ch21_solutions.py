import itertools
import random
import unittest

import ch21_examples as ex
import ch21_solutions as sol


def brute_cover(k, skills):
    full = (1 << k) - 1
    for r in range(len(skills) + 1):
        for pick in itertools.combinations(range(len(skills)), r):
            u = 0
            for v in pick:
                u |= skills[v]
            if u == full:
                return r
    return float("inf")


class TestChapter21Solutions(unittest.TestCase):
    def test_fewest_cover(self) -> None:
        self.assertEqual(sol.fewest_cover(0, []), (0, []))
        self.assertEqual(sol.fewest_cover(1, []), (float("inf"), []))
        self.assertEqual(sol.fewest_cover(1, [1]), (1, [0]))
        self.assertEqual(sol.fewest_cover(5, [0b00011, 0b01100, 0b10001, 0b10110, 0b01000]), (3, [0, 3, 4]))
        r = random.Random(21)
        for _ in range(300):
            k, p = r.randint(0, 5), r.randint(0, 6)
            skills = [r.randint(0, (1 << k) - 1) for _ in range(p)]
            count, chosen = sol.fewest_cover(k, skills)
            self.assertEqual(count, brute_cover(k, skills))
            if chosen:
                u = 0
                for v in chosen:
                    u |= skills[v]
                self.assertEqual((u, len(chosen)), ((1 << k) - 1, count))

    def test_set_only_round(self) -> None:
        d = ex.matrix(ex.BRANCHES, ex.TRAVEL)
        self.assertEqual((sol.set_only_round(d), ex.held_karp(d)[0]), (23, 21))
        self.assertEqual(sol.set_only_round([[0]]), 0)
        self.assertEqual(sol.set_only_round([[0, 4], [4, 0]]), 8)
        r = random.Random(2)
        for _ in range(100):
            n = r.randint(1, 6)
            dd = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    dd[i][j] = dd[j][i] = r.randint(1, 9)
            self.assertGreaterEqual(sol.set_only_round(dd), ex.brute(dd))

    def test_more_never_shorter_needs_triangle(self) -> None:
        d = ex.matrix(ex.BRANCHES, ex.TRAVEL)
        _, best = ex.held_karp_masks(d)
        self.assertEqual((best[0b01000][3], best[0b01010][3]), (10, 6))


if __name__ == "__main__":
    unittest.main()
