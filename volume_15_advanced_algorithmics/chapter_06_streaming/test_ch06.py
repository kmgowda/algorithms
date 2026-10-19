import random
import unittest
from collections import Counter

import ch06_examples as ex
import ch06_solutions as sol


class TestStreaming(unittest.TestCase):
    def test_guarantees(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            stream = [rng.choice("aabbbcdefg") for _ in range(rng.randint(1, 60))]
            counts = Counter(stream)
            maj = [x for x, c in counts.items() if 2 * c > len(stream)]
            if maj:
                self.assertEqual(ex.majority_vote(stream), maj[0])
            self.assertEqual(sol.majority_check(stream), maj[0] if maj else None)
            k = rng.randint(2, 5)
            mg = ex.misra_gries(stream, k)
            for x, c in counts.items():
                if c > len(stream) / k:
                    self.assertIn(x, mg)
                self.assertLessEqual(mg.get(x, 0), c)
                self.assertGreaterEqual(mg.get(x, 0), c - len(stream) / k)
            cm = ex.CountMin(50, 3)
            for x in stream:
                cm.add(x)
            for x, c in counts.items():
                self.assertGreaterEqual(cm.estimate(x), c)
            vals = [rng.randint(0, 9) for _ in range(rng.randint(1, 20))]
            w = rng.randint(1, 5)
            avgs = sol.sliding_window_average(vals, w)
            for i, a in enumerate(avgs):
                window = vals[max(0, i - w + 1):i + 1]
                self.assertAlmostEqual(a, sum(window) / len(window))
        for n in (50, 2000, 50000):
            self.assertLess(abs(ex.hyperloglog(range(n)) - n) / n, 0.1)
        self.assertLess(abs(ex.hyperloglog(list(range(1000)) * 5) - 1000) / 1000, 0.1)
        self.assertEqual(len(sol.sample_stream(range(1000), 10, rng)), 10)

    def test_examples(self) -> None:
        est, exact = ex.unique_visitors([f"u{i % 5000}" for i in range(40000)])
        self.assertEqual(exact, 5000)
        self.assertLess(abs(est - 5000) / 5000, 0.1)


if __name__ == "__main__":
    unittest.main()
