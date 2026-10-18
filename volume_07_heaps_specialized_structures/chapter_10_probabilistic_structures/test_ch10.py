import random
import unittest
from collections import Counter

import ch10_examples as ex
import ch10_solutions as sol


class TestBloom(unittest.TestCase):
    def test_no_false_negatives_and_rate(self) -> None:
        bf = ex.BloomFilter(2000, 0.02)
        items = [f"item{i}" for i in range(2000)]
        for x in items:
            bf.add(x)
        self.assertTrue(all(bf.might_contain(x) for x in items))
        rate = sum(bf.might_contain(f"other{i}") for i in range(20_000)) / 20_000
        self.assertLess(rate, 0.04)
        self.assertLess(sol.measured_false_positive(1000, 0.01), 0.025)

    def test_crawler(self) -> None:
        fetched = ex.crawler_skip_seen([f"page{i % 300}" for i in range(1000)])
        self.assertLessEqual(fetched, 300)
        self.assertGreater(fetched, 290)


class TestSketches(unittest.TestCase):
    def test_count_min_never_underestimates(self) -> None:
        rng = random.Random(1)
        stream = [f"w{int(rng.paretovariate(1.2))}" for _ in range(5000)]
        cms = ex.CountMinSketch(300, 5)
        for x in stream:
            cms.add(x)
        true = Counter(stream)
        for w, c in true.items():
            est = cms.estimate(w)
            self.assertGreaterEqual(est, c)
            self.assertLessEqual(est - c, 2 * len(stream) * 2.72 / 300)

    def test_hyperloglog(self) -> None:
        for n in (100, 5000, 50_000):
            h = ex.HyperLogLog(p=10)
            for i in range(n):
                h.add(f"v{i}")
                h.add(f"v{i}")                     # duplicates don't count
            self.assertLess(abs(h.count() - n) / n, 0.12)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        m, k = sol.bloom_size(10**6, 0.01)
        self.assertEqual(k, 7)
        self.assertAlmostEqual(m / 10**6, 9.59, places=1)
        self.assertAlmostEqual(sol.predicted_false_positive(m, k, 10**6), 0.01, places=3)
        hh = sol.heavy_hitters(["a"] * 50 + ["b"] * 30 + [f"x{i}" for i in range(200)], 25)
        self.assertIn("a", hh)
        self.assertIn("b", hh)


if __name__ == "__main__":
    unittest.main()
