import random
import unittest

import ch20_examples as ex
import ch20_solutions as sol


def brute_time(minutes: list[int], m: int) -> int:
    t = 0
    while sum(t // each for each in minutes) < m:
        t += 1
    return t


class TestChapter20Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.shelving_time([3], 0), 0)
        self.assertEqual(sol.shelving_time([3], 1), 3)
        self.assertEqual(sol.shelving_time([1], 5), 5)
        self.assertEqual(sol.shelving_time([4, 4], 2), 4)

    def test_worked_example(self) -> None:
        self.assertEqual(sol.shelving_time([3, 5, 8], 20), 32)
        self.assertEqual(sum(31 // t for t in (3, 5, 8)), 19)

    def test_against_brute_force(self) -> None:
        rng = random.Random(20)
        for _ in range(500):
            minutes = [rng.randint(1, 9) for _ in range(rng.randint(1, 4))]
            m = rng.randint(0, 40)
            self.assertEqual(sol.shelving_time(minutes, m), brute_time(minutes, m))

    def test_greedy_is_optimal(self) -> None:
        """Thinking Problem 1: greedy loading uses the fewest trips of any split of the boxes in order."""
        def best_split(boxes, cap):
            best = [0] + [None] * len(boxes)            # best[i]: fewest trips for the first i boxes
            for i in range(1, len(boxes) + 1):
                for j in range(i):
                    if best[j] is not None and sum(boxes[j:i]) <= cap:
                        if best[i] is None or best[j] + 1 < best[i]:
                            best[i] = best[j] + 1
            return best[-1]
        rng = random.Random(201)
        for _ in range(500):
            boxes = [rng.randint(1, 9) for _ in range(rng.randint(1, 8))]
            cap = rng.randint(max(boxes), sum(boxes))
            self.assertEqual(ex.trips_needed(boxes, cap), best_split(boxes, cap))

    def test_low_start_bug(self) -> None:
        """Thinking Problem 3: starting the range at 1 lets a too-weak trolley pass the check."""
        trace = []
        wrong = ex.first_true(1, 3, lambda c: ex.trips_needed([3], c) <= 2, trace)
        self.assertEqual((wrong, trace), (1, [(1, 3, 2, True), (1, 2, 1, True)]))
        self.assertEqual(ex.smallest_capacity([3], 2), 3)
        self.assertEqual(ex.first_true(1, 44, lambda c: ex.trips_needed(ex.BOXES, c) <= 8), 5)
        self.assertEqual(ex.smallest_capacity(ex.BOXES, 8), 9)


if __name__ == "__main__":
    unittest.main()
