"""Tests for ch24_compare (Section 24.9): every strategy finds every key, and the printed look counts are pinned."""
import random
import unittest

import ch24_compare as c


class TestCompare(unittest.TestCase):
    def test_every_strategy_finds_every_key(self):
        rng = random.Random(3)
        for n in range(1, 40):
            a = sorted(rng.sample(range(1000), n))
            for key in a:
                for name, f in c.STRATEGIES.items():
                    pos = f(a, key)
                    self.assertEqual(a[pos[-1]], key, (name, n, key))

    def test_printed_counts(self):
        r = c.compare(30)
        self.assertEqual({k: len(v) for k, v in r.items()},
                         {"brute force": 3, "halves, both kept": 3, "halves, one kept": 4, "doubling, then halving": 4})
        r = c.compare(150)
        self.assertEqual({k: len(v) for k, v in r.items()},
                         {"brute force": 15, "halves, both kept": 15, "halves, one kept": 4,
                          "doubling, then halving": 8})
        big = list(range(1_000_000))
        self.assertEqual([len(c.brute_force(big, 3)), len(c.halves_one(big, 3)), len(c.doubling(big, 3))], [4, 20, 3])
        self.assertEqual([len(c.halves_one(big, 700_000)), len(c.doubling(big, 700_000))], [19, 40])

    def test_every_case(self):
        self.assertEqual(c.brute_force([], 5), [])
        self.assertEqual(c.halves_both([], 5), [])
        self.assertEqual(c.halves_one([], 5), [])
        self.assertEqual(c.doubling([7], 7), [0])
        self.assertEqual(c.doubling([], 7), [])
        self.assertEqual(len(c.halves_one([1, 2, 3], 9)), 2)


if __name__ == "__main__":
    unittest.main()
