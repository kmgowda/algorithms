import random
import unittest

import ch03_examples as ex


class TestChapter03(unittest.TestCase):
    def test_rotated(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            base = sorted(rng.sample(range(100), rng.randint(1, 15)))
            k = rng.randrange(len(base))
            a = base[k:] + base[:k]
            self.assertEqual(a[ex.find_rotation(a)], min(a))
            for key in range(-1, 101):
                i = ex.search_rotated(a, key)
                self.assertEqual(i == -1, key not in a)
                if i != -1:
                    self.assertEqual(a[i], key)

    def test_examples(self) -> None:
        self.assertEqual(ex.find_rotation(ex.ROTATED), 5)
        t = []
        self.assertEqual(ex.search_rotated(ex.ROTATED, 31, t), 7)
        self.assertEqual([x[:3] for x in t], [(0, 8, 4), (5, 8, 6), (7, 8, 7)])
        t = []
        self.assertEqual(ex.staircase_search(ex.GRID, 58, t), (3, 1))
        self.assertEqual(len(t), 6)
        t = []
        self.assertIsNone(ex.staircase_search(ex.GRID, 50, t))
        self.assertEqual(len(t), 7)

    def test_every_case(self) -> None:
        r, s = ex.ROTATED, sorted(ex.ROTATED)
        rows = [(s, 63, 5, 3), ([91] + s[:-1], 25, 2, 3), (r, 70, 2, 3), (r, 31, 7, 3), (r, 91, 4, 1), (r, 65, -1, 4),
                ([47], 47, 0, 1)]
        for a, key, pos, looks in rows:
            t = []
            self.assertEqual(ex.search_rotated(a, key, t), pos)
            self.assertEqual(len(t), looks)
        dup = [47, 12, 47, 47, 47]
        self.assertEqual(ex.search_rotated(dup, 12), -1)                 # the documented failure
        self.assertEqual(ex.search_rotated_with_duplicates(dup, 12), 1)  # and its fix
        for key, cell, looks in [(47, (0, 3), 1), (35, (3, 0), 7), (12, (0, 0), 4), (91, (3, 3), 4), (50, None, 7),
                                 (5, None, 4), (99, None, 4)]:
            t = []
            self.assertEqual(ex.staircase_search(ex.GRID, key, t), cell)
            self.assertEqual(len(t), looks)

    def test_duplicates_fix_random(self) -> None:
        rng = random.Random(4)
        for _ in range(500):
            base = sorted(rng.randint(0, 5) for _ in range(rng.randint(1, 12)))
            k = rng.randrange(len(base))
            a = base[k:] + base[:k]
            for key in range(-1, 7):
                i = ex.search_rotated_with_duplicates(a, key)
                self.assertEqual(i != -1, key in a)
                if i != -1:
                    self.assertEqual(a[i], key)

    def test_staircase_random(self) -> None:
        rng = random.Random(2)
        for _ in range(100):
            r, c = rng.randint(1, 6), rng.randint(1, 6)
            g = [[0] * c for _ in range(r)]
            for i in range(r):
                for j in range(c):
                    g[i][j] = max(g[i - 1][j] if i else 0, g[i][j - 1] if j else 0) + rng.randint(1, 3)
            values = {v for row in g for v in row}
            for key in range(0, max(values) + 2):
                found = ex.staircase_search(g, key)
                self.assertEqual(found is not None, key in values)

    def test_overnight_log(self) -> None:
        rng = random.Random(3)
        times = sorted(rng.sample(range(24 * 60), 500))
        ring = times[200:] + times[:200]
        for t in range(0, 24 * 60, 37):
            i = ex.first_at_or_after(ring, t)
            later = [x for x in times if x >= t]
            self.assertEqual(None if i is None else ring[i], later[0] if later else None)

    def test_rotation_point_trace(self) -> None:
        t = []
        self.assertEqual(ex.find_rotation(ex.ROTATED, t), 5)
        self.assertEqual(t, [(0, 8, 4, 91, 47), (5, 8, 6, 25, 47), (5, 6, 5, 12, 25)])
        self.assertEqual(ex.find_rotation([]), 0)
        self.assertEqual(ex.find_rotation([5]), 0)
        self.assertEqual(ex.find_rotation([47, 47, 47, 12, 47]), 0)                 # duplicates fool it
        self.assertEqual(ex.find_rotation_with_duplicates([47, 47, 47, 12, 47]), 3)
        for a in ([], [5], [12, 25, 31], [47, 12, 47, 47, 47], [3, 3, 3]):
            if a:
                self.assertEqual(a[ex.find_rotation_with_duplicates(a)], min(a))


if __name__ == "__main__":
    unittest.main()
