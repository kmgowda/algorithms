import random
import unittest
from collections import Counter

import ch18_solutions as sol


class TestSameMultiset(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        rng = random.Random(1)
        self.assertTrue(sol.same_multiset([], [], 3, rng))
        self.assertFalse(sol.same_multiset([], [0], 3, rng))
        self.assertTrue(sol.same_multiset([7], [7], 3, rng))
        self.assertFalse(sol.same_multiset([7], [8], 3, rng))
        self.assertTrue(sol.same_multiset([7], [8], 0, rng))         # zero rounds checks nothing but the lengths

    def test_counts_matter(self) -> None:
        rng = random.Random(2)
        self.assertFalse(sol.same_multiset([1, 1, 2], [1, 2, 2], 2, rng))
        pile = [58, 25, 91, 12, 70, 47, 84, 31, 63]
        self.assertTrue(sol.same_multiset(pile, sorted(pile), 2, rng))

    def test_against_counter(self) -> None:
        r = random.Random(18)
        for _ in range(500):
            a = [r.randint(0, 4) for _ in range(r.randint(0, 6))]
            b = list(a)
            r.shuffle(b)
            if b and r.random() < 0.5:
                b[r.randrange(len(b))] = r.randint(0, 4)
            self.assertEqual(sol.same_multiset(a, b, 2, r), Counter(a) == Counter(b), (a, b))


if __name__ == "__main__":
    unittest.main()
