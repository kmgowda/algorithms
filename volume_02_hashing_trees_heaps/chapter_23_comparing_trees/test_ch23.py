import random
import unittest

import ch23_examples as ex


class TestChapter52(unittest.TestCase):
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
