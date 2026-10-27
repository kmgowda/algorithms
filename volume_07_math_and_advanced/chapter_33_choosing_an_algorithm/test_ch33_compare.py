"""Tests for ch33_compare (Section 33.11): every method's cover is valid, the exact ones are smallest, and the
printed counts are pinned."""
import unittest

import ch33_compare as c


class TestCompare(unittest.TestCase):
    def test_town(self):
        r = c.compare()
        for key in ("brute", "branching"):
            self.assertEqual(len(r[key][0]), 4)
        for cover in (r["greedy"], r["matching"], r["lp"][1], r["local"][0], r["best"]):
            self.assertTrue(c.is_cover(cover, c.ROADS))
        self.assertEqual(r["brute"][1], 133)
        self.assertEqual(r["branching"][1], 31)
        self.assertEqual(len(r["greedy"]), 5)
        self.assertEqual(len(r["matching"]), 8)
        self.assertEqual(r["lp"][0], 4)
        self.assertEqual(len(r["lp"][1]), 8)
        self.assertLessEqual(len(r["matching"]), 2 * len(r["best"]))

    def test_local_orders(self):
        self.assertEqual(c.local_search_orders(), {4: 12768, 5: 21924, 6: 5628})

    def test_every_case(self):
        self.assertEqual(c.greedy_degree(["A"], []), [])
        self.assertEqual(c.local_search(["A", "B"], [("A", "B")])[0], ["B"])
        r = c.compare(["A", "B", "C"], [("A", "B"), ("B", "C")])
        self.assertEqual(r["best"], ["B"])
        self.assertEqual(r["greedy"], ["B"])


if __name__ == "__main__":
    unittest.main()
