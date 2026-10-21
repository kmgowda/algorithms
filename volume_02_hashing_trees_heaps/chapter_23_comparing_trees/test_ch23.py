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


if __name__ == "__main__":
    unittest.main()
