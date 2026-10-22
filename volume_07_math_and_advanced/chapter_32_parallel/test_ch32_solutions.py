import itertools
import random
import unittest

import ch32_examples as ex
import ch32_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_rounds(self) -> None:
        for n in range(1, 300):
            total, work, rounds = ex.tree_sum(list(range(n)))
            self.assertEqual((work, rounds), (n - 1, sol.rounds_predicted(n)))

    def test_filter(self) -> None:
        self.assertEqual(sol.parallel_filter([58, 25, 91, 12, 70, 47, 84, 31, 63], 50), ([58, 91, 70, 84, 63], 6))
        self.assertEqual(sol.parallel_filter([], 5)[0], [])
        r = random.Random(32)
        for _ in range(100):
            v = [r.randint(0, 99) for _ in range(r.randint(1, 40))]
            self.assertEqual(sol.parallel_filter(v, 50)[0], [x for x in v if x > 50])

    def test_in_place_bug(self) -> None:
        v = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertNotEqual(sol.scan_in_place_bug(v), list(itertools.accumulate(v)))
        self.assertEqual(ex.prefix_sums_parallel(v)[0], list(itertools.accumulate(v)))
        self.assertEqual(sol.scan_in_place_bug([1, 1, 1, 1]), [1, 2, 4, 6])


if __name__ == "__main__":
    unittest.main()
