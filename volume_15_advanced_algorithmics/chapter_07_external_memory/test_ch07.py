import random
import tempfile
import unittest
from collections import Counter

import ch07_examples as ex
import ch07_solutions as sol


class TestExternal(unittest.TestCase):
    def test_external_sort(self) -> None:
        rng = random.Random(1)
        for _ in range(20):
            data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 300))]
            mem = rng.randint(1, 40)
            with tempfile.TemporaryDirectory() as d:
                out, runs, io = ex.external_sort(data, mem, d)
            self.assertEqual(out, sorted(data))
            self.assertEqual(runs, -(-len(data) // mem))
            self.assertEqual(io, 4 * len(data))
        self.assertEqual(ex.block_reads(1000, 10, "sequential", rng), 100)
        self.assertGreater(ex.block_reads(1000, 10, "random", rng), 500)

    def test_map_reduce(self) -> None:
        rng = random.Random(2)
        words = ["a", "b", "c", "d"]
        docs = [" ".join(rng.choice(words) for _ in range(rng.randint(0, 10))) for _ in range(30)]
        self.assertEqual(ex.word_count(docs), dict(Counter(w for d in docs for w in d.split())))
        for workers in (1, 3, 7):
            self.assertEqual(ex.map_reduce(docs, lambda d: [(w, 1) for w in d.split()], lambda _, c: sum(c), workers),
                             ex.word_count(docs))
        self.assertEqual(sol.inverted_index({"a": "red fish", "b": "blue fish"}), {"blue": ["b"], "fish": ["a", "b"], "red": ["a"]})
        self.assertEqual(sol.max_temperature(["Pune,31", "Delhi,40", "Pune,35"]), {"Pune": 35, "Delhi": 40})
        self.assertEqual(sol.merge_passes(10 ** 9, 10 ** 7, 10), 3)
        self.assertEqual(sol.merge_passes(100, 100, 2), 1)


if __name__ == "__main__":
    unittest.main()
