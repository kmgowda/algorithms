import itertools
import random
import unittest

import ch15_examples as ex


class TestChapter15(unittest.TestCase):
    def test_patterns(self) -> None:
        for x in range(-3, 5):
            for n in range(0, 30):
                self.assertEqual(ex.power(x, n), x ** n)
        for k in range(0, 6):
            items = list("ABCDEF"[:k])
            self.assertEqual(sorted(map(tuple, ex.permutations(items))), sorted(itertools.permutations(items)))
            self.assertEqual(sorted(map(tuple, ex.subsets(items))),
                             sorted(c for r in range(k + 1) for c in itertools.combinations(items, r)))
        rng = random.Random(1)
        for _ in range(300):
            xs = sorted(rng.sample(range(100), rng.randint(0, 15)))
            t = rng.randint(0, 99)
            self.assertEqual(ex.search(xs, t, 0, len(xs) - 1), xs.index(t) if t in xs else -1)
        self.assertEqual(ex.power(3, 13), 1_594_323)


if __name__ == "__main__":
    unittest.main()
