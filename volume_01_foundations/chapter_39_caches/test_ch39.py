import random
import unittest
from collections import OrderedDict

import ch39_examples as ex


class TestChapter39(unittest.TestCase):
    def test_against_ordered_dict(self) -> None:
        rng = random.Random(1)
        for cap in (1, 2, 3, 5):
            c, ref = ex.LRUCache(cap), OrderedDict()
            for _ in range(2000):
                k = rng.randint(0, 8)
                if rng.random() < 0.5:
                    got = c.get(k)
                    exp = ref.get(k)
                    if k in ref:
                        ref.move_to_end(k)
                    self.assertEqual(got, exp)
                else:
                    c.put(k, k * 10)
                    ref[k] = k * 10
                    ref.move_to_end(k)
                    if len(ref) > cap:
                        ref.popitem(last=False)
                self.assertEqual(c.keys_oldest_first(), list(ref))

    def test_examples(self) -> None:
        req = ["Maps", "Ocean", "Maps", "Clocks", "Stars", "Maps", "Ocean", "Stars"]
        self.assertEqual((ex.count_hits(req, 3, "lru"), ex.count_hits(req, 3, "fifo")), (3, 2))
        seq = list("ABACBA")
        self.assertEqual((ex.count_hits(seq, 2, "lru"), ex.count_hits(seq, 2, "fifo")), (1, 2))
        self.assertEqual(ex.count_hits(list("ABCD") * 10, 3, "lru"), 0)
        views = ex.popular_requests(10_000, items=5000, seed=3)
        self.assertGreater(ex.count_hits(views, 500, "lru") / len(views), 0.5)


if __name__ == "__main__":
    unittest.main()
