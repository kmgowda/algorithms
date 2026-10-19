import itertools
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestParallel(unittest.TestCase):
    def test_correctness(self) -> None:
        rng = random.Random(1)
        self.assertEqual(ex.parallel_count_primes(5000, 1), ex.parallel_count_primes(5000, 4))
        self.assertEqual(ex.count_primes_in((0, 100)), 25)
        data = [rng.randint(0, 1000) for _ in range(5000)]
        self.assertEqual(ex.parallel_merge_sort(data, 3), sorted(data))
        self.assertEqual(ex.parallel_merge_sort([], 3), [])
        for _ in range(100):
            vals = [rng.randint(-9, 9) for _ in range(rng.randint(1, 40))]
            out, rounds, work = ex.prefix_sums_rounds(vals)
            self.assertEqual(out, list(itertools.accumulate(vals)))
            self.assertEqual(rounds, (len(vals) - 1).bit_length())
            self.assertEqual(sol.parallel_max(vals, rng.randint(1, 5)), max(vals))
            n = rng.randint(1, 100)
            w, s = sol.work_and_span_sum(n)
            self.assertEqual(w, n - 1)
            self.assertEqual(s, (n - 1).bit_length())

    def test_amdahl(self) -> None:
        self.assertAlmostEqual(ex.amdahl_speedup(0.9, 1), 1.0)
        self.assertLess(ex.amdahl_speedup(0.9, 10 ** 6), 10)
        self.assertEqual(sol.max_useful_processors(0.9, 5), 9)
        self.assertIsNone(sol.max_useful_processors(0.9, 10))
        self.assertEqual(ex.render_tiles(5, 2), ex.parallel_count_primes(10000, 1))


if __name__ == "__main__":
    unittest.main()
