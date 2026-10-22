import itertools
import random
import unittest

import ch16_examples as ex
import ch16_solutions as sol


def brute(intervals) -> int:
    return sum(1 for (a, b), (c, d) in itertools.combinations(intervals, 2) if a < d and c < b)


class TestOverlappingPairs(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.overlapping_pairs([]), 0)
        self.assertEqual(sol.overlapping_pairs([(9, 10)]), 0)
        self.assertEqual(sol.overlapping_pairs([(9, 10), (10, 11)]), 0)       # back to back
        self.assertEqual(sol.overlapping_pairs([(9, 11), (9, 11)]), 1)        # identical

    def test_bookings(self) -> None:
        self.assertEqual(sol.overlapping_pairs(ex.BOOKINGS), brute(ex.BOOKINGS))

    def test_against_brute_force(self) -> None:
        r = random.Random(16)
        for _ in range(400):
            iv = []
            for _ in range(r.randint(0, 8)):
                s = r.randint(0, 10)
                iv.append((s, s + r.randint(1, 5)))
            self.assertEqual(sol.overlapping_pairs(iv), brute(iv), iv)


if __name__ == "__main__":
    unittest.main()
