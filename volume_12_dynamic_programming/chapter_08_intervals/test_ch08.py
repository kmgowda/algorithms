import itertools
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


def brute_balloons(nums):
    best = 0
    for order in itertools.permutations(range(len(nums))):
        alive, total = list(range(len(nums))), 0
        for k in order:
            pos = alive.index(k)
            left = nums[alive[pos - 1]] if pos > 0 else 1
            right = nums[alive[pos + 1]] if pos + 1 < len(alive) else 1
            total += left * nums[k] * right
            alive.pop(pos)
        best = max(best, total)
    return best


def brute_bst(freq, lo=0, hi=None, depth=1):
    hi = len(freq) - 1 if hi is None else hi
    if lo > hi:
        return 0
    return min(freq[r] * depth + brute_bst(freq, lo, r - 1, depth + 1) + brute_bst(freq, r + 1, hi, depth + 1)
               for r in range(lo, hi + 1))


def brute_cuts(length, cuts):
    best = None
    for order in itertools.permutations(cuts):
        pieces, total = [(0, length)], 0
        for c in order:
            for idx, (a, b) in enumerate(pieces):
                if a < c < b:
                    total += b - a
                    pieces[idx:idx + 1] = [(a, c), (c, b)]
                    break
        best = total if best is None else min(best, total)
    return best or 0


class TestIntervals(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(60):
            dims = [rng.randint(1, 20) for _ in range(rng.randint(2, 7))]
            cost, brackets = ex.matrix_chain(dims)
            self.assertEqual(cost, sol.brute_matrix_chain(dims))
            self.assertEqual(brackets.count("A"), len(dims) - 1)
            nums = [rng.randint(1, 9) for _ in range(rng.randint(1, 6))]
            self.assertEqual(ex.burst_balloons(nums), brute_balloons(nums))
            freq = [rng.randint(1, 20) for _ in range(rng.randint(0, 6))]
            self.assertEqual(ex.optimal_bst_cost(freq), brute_bst(freq))
            length = rng.randint(2, 12)
            cuts = rng.sample(range(1, length), min(length - 1, rng.randint(1, 5)))
            self.assertEqual(ex.cut_stick(length, cuts), brute_cuts(length, cuts))

    def test_examples(self) -> None:
        self.assertEqual(ex.matrix_chain([10, 30, 5, 60]), (4500, "((A1 A2) A3)"))
        self.assertEqual(ex.burst_balloons([3, 1, 5, 8]), 167)
        self.assertEqual(ex.optimal_bst_cost([34, 8, 50]), 142)
        self.assertEqual(ex.cut_stick(7, [1, 3, 4, 5]), 16)
        self.assertEqual(sol.stone_merge_cost([4, 1, 2, 3]), 19)   # (1+2)=3, (3+3)=6, (4+6)=10
        self.assertEqual(sol.min_score_triangulation([3, 7, 4, 5]), 144)


if __name__ == "__main__":
    unittest.main()
