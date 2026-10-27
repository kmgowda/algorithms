"""Tests for ch30_compare (Section 30.10): the guarantees hold and the printed numbers are pinned."""
import unittest

import ch30_compare as c


class TestCompare(unittest.TestCase):
    def setUp(self):
        self.s = c.searches()

    def test_heavy_hitters(self):
        rows = {r[0]: r for r in c.heavy_hitters(self.s)}
        n, k = len(self.s), 50
        true = rows["exact dictionary"][2]
        self.assertEqual(true, 990)
        self.assertEqual(rows["exact dictionary"][1], 2001)
        mg, ss, cm = rows["Misra-Gries"][2], rows["Space-Saving"][2], rows["Count-Min"][2]
        self.assertTrue(true - n / k <= mg <= true)          # Misra-Gries never overcounts, undercounts <= n/k
        self.assertTrue(true <= ss <= true + n / k)          # Space-Saving never undercounts
        self.assertGreaterEqual(cm, true)                    # Count-Min never undercounts
        self.assertEqual((mg, ss, cm), (603, 990, 1001))

    def test_distinct(self):
        rows = {r[0]: r for r in c.distinct(self.s)}
        self.assertEqual(rows["exact set"][2], 2001)
        self.assertEqual([rows[k][2] for k in ("smallest 64 hashes", "Flajolet-Martin, 64 copies",
                                               "HyperLogLog, 1,024 registers")], [1758, 1812, 2016])

    def test_every_case(self):
        self.assertEqual(c.heavy_hitters(["dragons"], k=2, width=4, depth=1)[1][2], 1)
        self.assertEqual(c.distinct(["a", "a"])[0][2], 1)


if __name__ == "__main__":
    unittest.main()
