import itertools
import random
import unittest

import ch18_solutions as sol

BOXES = [(5, 4), (6, 4), (6, 7), (2, 3), (4, 5), (7, 8), (6, 6)]


def fits(a, b):
    return a[0] < b[0] and a[1] < b[1]


class TestChapter18Solutions(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(sol.longest_nesting(BOXES), (4, [(2, 3), (5, 4), (6, 6), (7, 8)]))
        self.assertEqual(sol.nesting_table(BOXES), 4)

    def test_smallest(self) -> None:
        self.assertEqual(sol.longest_nesting([]), (0, []))
        self.assertEqual(sol.longest_nesting([(3, 3)]), (1, [(3, 3)]))
        self.assertEqual(sol.longest_nesting([(3, 3), (3, 3)])[0], 1)
        self.assertEqual(sol.longest_nesting([(3, 1), (3, 2), (3, 3)])[0], 1)     # equal widths never nest
        self.assertEqual(sol.longest_nesting([(1, 3), (2, 3)])[0], 1)             # equal heights never nest

    def test_random_against_brute_force(self) -> None:
        r = random.Random(18)
        for _ in range(300):
            boxes = [(r.randint(1, 5), r.randint(1, 5)) for _ in range(r.randint(0, 7))]
            n, chain = sol.longest_nesting(boxes)
            want = max([0] + [k for k in range(1, len(boxes) + 1) for c in itertools.permutations(boxes, k)
                              if all(fits(a, b) for a, b in zip(c, c[1:]))]) if len(boxes) <= 5 else sol.nesting_table(boxes)
            self.assertEqual((n, sol.nesting_table(boxes)), (want, want))
            self.assertEqual(len(chain), n)
            self.assertTrue(all(fits(a, b) for a, b in zip(chain, chain[1:])))
            remaining = list(boxes)
            for b in chain:
                remaining.remove(b)


if __name__ == "__main__":
    unittest.main()
