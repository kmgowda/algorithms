import itertools
import random
import unittest

import ch21_examples as ex


class TestChapter21(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.check_subset(ex.PRICES, [0, 2, 4], 31), ex.find_subset(ex.PRICES, 31), ex.find_subset(ex.PRICES, 200)),
                         (True, ([0, 2, 4], 66), (None, 1024)))
        self.assertEqual(ex.has_independent_set(ex.TOWN, ex.ROADS, 4), ["Library", "Market", "Hospital", "Harbour"])
        self.assertIsNone(ex.has_independent_set(ex.TOWN, ex.ROADS, 5))

    def test_every_case(self) -> None:
        self.assertEqual((ex.find_subset([], 0), ex.find_subset([], 5)), (([], 1), (None, 1)))
        self.assertEqual((ex.check_subset([3], [0, 0], 6), ex.check_subset([3], [5], 3)), (False, False))
        self.assertEqual((ex.has_clique(["a"], set(), 1), ex.has_independent_set(["a", "b"], {("a", "b")}, 2)), (["a"], None))
        r = random.Random(21)
        for _ in range(100):
            vs = list(range(r.randint(1, 7)))
            es = {e for e in itertools.combinations(vs, 2) if r.random() < 0.4}
            k = r.randint(1, len(vs))
            direct = next((list(g) for g in itertools.combinations(vs, k) if not any(e in es for e in itertools.combinations(g, 2))), None)
            self.assertEqual(ex.has_independent_set(vs, es, k), direct)


if __name__ == "__main__":
    unittest.main()
