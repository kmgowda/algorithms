import itertools
import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


def brute_steady(v: list[int], limit: int) -> int:
    return max((j - i for i in range(len(v)) for j in range(i + 1, len(v) + 1)
                if max(v[i:j]) - min(v[i:j]) <= limit), default=0)


class TestThinkingProblems(unittest.TestCase):
    def test_marker_pairs_are_too_few(self) -> None:
        # Problem 1: with front fixed, the lengths 0..c need c + 1 different backs, but only c exist.
        for c in range(1, 7):
            for front in range(c):
                backs = {(front + count) % c for count in range(c + 1)}
                self.assertEqual(len(backs), c)
            r = ex.RingBuffer(c)
            self.assertEqual((r.front, r.back), (0, 0))
            for x in range(c):
                r.enqueue(x)
            self.assertEqual((r.front, r.back), (0, 0))         # full looks exactly like empty

    def test_steady_smallest(self) -> None:
        self.assertEqual(sol.longest_steady_stretch([], 3), 0)
        self.assertEqual(sol.longest_steady_stretch([7], 0), 1)
        self.assertEqual(sol.longest_steady_stretch([7, 7, 7], 0), 3)
        self.assertEqual(sol.longest_steady_stretch([1, 2], -1), 0)

    def test_steady_example_and_brute_force(self) -> None:
        self.assertEqual(sol.longest_steady_stretch([3, 1, 4, 1, 5, 9, 2, 6], 3), 4)
        rng = random.Random(9)
        for _ in range(500):
            v = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
            limit = rng.randint(0, 6)
            self.assertEqual(sol.longest_steady_stretch(v, limit), brute_steady(v, limit))

    def test_overwrite_bug(self) -> None:
        r = sol.OverwriteRingBuggy(3)
        for x in "ABCD":
            r.log(x)
        self.assertEqual((r.slots, r.front, r.oldest()), (["D", "B", "C"], 0, "D"))   # the oldest kept is B


if __name__ == "__main__":
    unittest.main()
