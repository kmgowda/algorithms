import math
import random
import unittest

import ch22_solutions as sol


class TestChapter22Solutions(unittest.TestCase):
    def test_example(self) -> None:
        r = sol.Reel(range(3, 3000, 3))
        self.assertEqual(sol.reel_length(r), 999)
        self.assertEqual(r.reads, 21)

    def test_smallest_inputs(self) -> None:
        for n, reads in [(0, 1), (1, 2), (2, 3), (3, 5)]:
            r = sol.Reel(range(n))
            self.assertEqual(sol.reel_length(r), n)
            self.assertEqual(r.reads, reads)

    def test_against_len(self) -> None:
        rng = random.Random(22)
        for n in list(range(0, 300)) + [rng.randint(300, 100_000) for _ in range(50)]:
            r = sol.Reel(sorted(rng.sample(range(10 * n + 1), n)))
            self.assertEqual(sol.reel_length(r), n)
            if n >= 2:
                self.assertEqual(r.reads, 2 * math.ceil(math.log2(n)) + 1)      # 1 + gallop + halving


if __name__ == "__main__":
    unittest.main()
