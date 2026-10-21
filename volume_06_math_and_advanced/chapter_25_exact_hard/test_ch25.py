import itertools
import random
import unittest

import ch25_examples as ex


class TestChapter25(unittest.TestCase):
    def test_examples(self) -> None:
        c = [0]
        self.assertEqual((ex.cover_branching(ex.ROADS, 4, c), c[0], ex.cover_brute(ex.TOWN, ex.ROADS, 4)[1]), (["School", "Park", "Station", "Museum"], 31, 133))
        c = [0]
        self.assertEqual((ex.cover_branching(ex.ROADS, 3, c), c[0]), (None, 15))
        r = random.Random(25)
        vals = [r.randint(1, 10 ** 6) for _ in range(24)]
        self.assertEqual((ex.subset_sum_mitm(vals, sum(vals[::3])), ex.subset_sum_mitm(vals, 1)), ((True, 8192), (False, 8192)))

    def test_every_case(self) -> None:
        self.assertEqual((ex.cover_branching([], 0, [0]), ex.cover_branching([("a", "b")], 0, [0])), ([], None))
        self.assertEqual((ex.subset_sum_mitm([], 0), ex.subset_sum_mitm([], 3), ex.subset_sum_mitm([5], 5)), ((True, 2), (False, 2), (True, 3)))
        r = random.Random(1)
        for _ in range(100):
            vs = list(range(7))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.35]
            k = r.randint(0, 5)
            self.assertEqual(ex.cover_branching(es, k, [0]) is None, ex.cover_brute(vs, es, k)[0] is None)
            vals = [r.randint(1, 20) for _ in range(r.randint(0, 8))]
            t = r.randint(0, 60)
            want = any(sum(c) == t for n in range(len(vals) + 1) for c in itertools.combinations(vals, n))
            self.assertEqual(ex.subset_sum_mitm(vals, t)[0], want)


if __name__ == "__main__":
    unittest.main()
