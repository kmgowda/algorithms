import itertools
import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


def brute(cost):
    n = len(cost)
    return min(max(cost[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))


class TestChapter11Solutions(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(sol.bottleneck_assignment(ex.MINUTES), (2, [0, 3, 1, 2]))
        self.assertEqual(sol.bottleneck_assignment(ex.SHELVING)[0], 2)
        self.assertEqual(sol.bottleneck_assignment([[1, 6], [5, 9]]), (6, [1, 0]))
        self.assertEqual(ex.hungarian([[1, 6], [5, 9]]), (10, [0, 1]))     # cheapest total, but a 9-minute trip

    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.bottleneck_assignment([]), (0, []))
        self.assertEqual(sol.bottleneck_assignment([[4]]), (4, [0]))
        self.assertEqual(sol.bottleneck_assignment([[3, 3], [3, 3]])[0], 3)   # all ties

    def test_against_brute_force(self) -> None:
        rng = random.Random(11)
        for _ in range(200):
            n = rng.randint(1, 5)
            cost = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]
            t, pick = sol.bottleneck_assignment(cost)
            self.assertEqual(t, brute(cost))
            self.assertEqual(sorted(pick), list(range(n)))
            self.assertEqual(max(cost[i][pick[i]] for i in range(n)), t)

    def test_matched_desks_is_not_a_cover(self) -> None:
        self.assertEqual(sol.uncovered(ex.CAN_DO_SIX, sol.matched_desks(ex.CAN_DO_SIX)), [("Eva", "Lost property")])
        _, cover = ex.konig_cover(ex.CAN_DO_SIX)
        self.assertEqual(sol.uncovered(ex.CAN_DO_SIX, cover), [])
        self.assertEqual(sol.uncovered(ex.CAN_DO, sol.matched_desks(ex.CAN_DO)), [])   # all desks used: no gap


if __name__ == "__main__":
    unittest.main()
