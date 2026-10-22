import sys
import random
import unittest

import ch23_examples as ex


class TestChapter52(unittest.TestCase):
    def test_every_case(self) -> None:
        import random
        sys.setrecursionlimit(30_000)
        r = random.Random(1).sample(range(10 ** 6), 1000)
        rows = [([], [-1, -1, -1, 0]), ([7], [0, 0, 0, 0]), ([5] * 1000, [0, 0, 0, 0]), (r, [20, 11, 12, 1]),
                (sorted(r), [999, 9, 16, 1]), (sorted(r, reverse=True), [999, 9, 16, 1])]
        for keys, heights in rows:
            m = ex.measure(keys, keys[:50])
            self.assertEqual([v["height"] for v in m.values()][:4], heights)
            self.assertTrue(all(v["found"] == len(keys[:50]) for v in m.values()))

    def test_all_structures_agree(self) -> None:
        rng = random.Random(1)
        keys = rng.sample(range(10 ** 5), 2000)
        lookups = keys[:500] + [k + 10 ** 5 for k in keys[:500]]
        for order in (keys, sorted(keys)):
            r = ex.measure(order, lookups)
            self.assertEqual({v["found"] for v in r.values()}, {500})
            self.assertLessEqual(r["AVL"]["height"], 16)
            self.assertLessEqual(r["red-black"]["height"], 22)
        self.assertEqual(ex.measure(sorted(keys), lookups)["plain BST"]["height"], 1999)

    def test_repair_work(self) -> None:
        """Section 23.5: rotations are close; the AVL cost is the height recomputed at every level."""
        self.assertEqual(ex.repair_work([]), {"AVL rotations": 0, "AVL height updates": 0, "red-black rotations": 0})
        self.assertEqual(ex.repair_work([12, 25, 31, 47, 58, 63, 70])["AVL rotations"], 4)
        rng = random.Random(1)
        keys = rng.sample(range(10 ** 6), 10_000)
        w = ex.repair_work(keys)
        self.assertEqual((w["AVL rotations"], w["AVL height updates"], w["red-black rotations"]), (6799, 134780, 5635))


if __name__ == "__main__":
    unittest.main()
