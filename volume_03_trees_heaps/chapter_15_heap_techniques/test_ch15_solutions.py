import itertools
import random
import unittest

import ch15_examples as ex
import ch15_solutions as sol


def brute(lists):
    if not lists or any(not l for l in lists):
        return None
    best = None
    for pick in itertools.product(*lists):
        w = (min(pick), max(pick))
        if best is None or w[1] - w[0] < best[1] - best[0]:
            best = w
    return best


class TestChapter15Solutions(unittest.TestCase):
    def test_smallest_window(self) -> None:
        self.assertIsNone(sol.smallest_window([]))
        self.assertIsNone(sol.smallest_window([[1, 2], []]))
        self.assertEqual(sol.smallest_window([[5]]), (5, 5))
        self.assertEqual(sol.smallest_window([[4, 9]]), (4, 4))
        self.assertEqual(sol.smallest_window([[3], [8]]), (3, 8))
        self.assertEqual(sol.smallest_window([[12, 47, 84], [25, 31, 91], [58, 63, 70]]), (70, 91))
        rng = random.Random(4)
        for _ in range(300):
            lists = [sorted(rng.sample(range(60), rng.randint(1, 4))) for _ in range(rng.randint(1, 4))]
            got, want = sol.smallest_window(lists), brute(lists)
            self.assertEqual(got[1] - got[0], want[1] - want[0])
            self.assertTrue(all(any(got[0] <= v <= got[1] for v in l) for l in lists))

    def test_cumulative_binding_is_not_optimal(self) -> None:
        self.assertEqual(sol.cumulative_bind_cost([]), 0)
        self.assertEqual(sol.cumulative_bind_cost([7]), 0)
        self.assertEqual(sol.cumulative_bind_cost([1, 1, 1, 1]), 9)
        self.assertEqual(ex.join_cost([1, 1, 1, 1])[0], 8)
        self.assertEqual(sol.cumulative_bind_cost([2, 3, 4, 6]), ex.join_cost([2, 3, 4, 6])[0])


if __name__ == "__main__":
    unittest.main()
