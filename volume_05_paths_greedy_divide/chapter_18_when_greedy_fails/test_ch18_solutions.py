import itertools
import random
import unittest

import ch18_examples as ex
import ch18_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_first_pick_bound(self) -> None:
        r = random.Random(18)
        for _ in range(100):
            universe = set(range(r.randint(1, 8)))
            sets = {f"s{i}": {x for x in universe if r.random() < 0.4} for i in range(r.randint(1, 6))}
            sets["all"] = set(universe) if r.random() < 0.2 else sets.get("s0", set())
            if set().union(*sets.values()) != universe:
                continue
            opt = len(ex.smallest_cover(universe, sets))
            first = ex.greedy_cover(universe, sets)[0]
            self.assertGreaterEqual(len(sets[first]) * opt, len(universe))

    def test_coin_systems(self) -> None:
        self.assertEqual((sol.greedy_change([1, 3, 4], 6), sol.fewest_coins([1, 3, 4], 6)[6]), ([4, 1, 1], 2))
        self.assertIsNone(sol.greedy_always_best([1, 2, 5, 10, 20, 50, 100, 200], 1000))
        self.assertEqual((sol.greedy_always_best([1, 3, 4], 100), sol.greedy_always_best([1, 10, 25], 100)), (6, 30))
        self.assertIsNone(sol.greedy_change([5], 3))


if __name__ == "__main__":
    unittest.main()
