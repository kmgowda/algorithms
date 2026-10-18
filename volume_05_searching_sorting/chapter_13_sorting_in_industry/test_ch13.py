import os
import random
import tempfile
import unittest

import ch13_examples as ex
import ch13_solutions as sol


class TestExternalSort(unittest.TestCase):
    def test_external_sort(self) -> None:
        rng = random.Random(1)
        for limit in (1, 7, 100, 5000):
            data = [rng.randint(-500, 500) for _ in range(rng.randint(0, 2000))]
            self.assertEqual(ex.external_sort(data, limit), sorted(data))

    def test_runs_written(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            paths = ex.write_sorted_runs(range(25, 0, -1), 10, folder)
            self.assertEqual(len(paths), 3)
            self.assertTrue(all(os.path.exists(p) for p in paths))
            self.assertEqual(list(ex.merge_runs(paths)), list(range(1, 26)))

    def test_passes(self) -> None:
        self.assertEqual(ex.merge_passes(10**10, 10**7, 100), 2)
        self.assertEqual(ex.merge_passes(100, 100, 2), 0)
        self.assertEqual(ex.merge_passes(800, 100, 2), 3)


class TestOrderBy(unittest.TestCase):
    def test_order_by(self) -> None:
        rng = random.Random(2)
        rows = [{"city": rng.choice(["Agra", "Pune", "Goa"]), "total": rng.randint(0, 9), "id": i} for i in range(50)]
        got = ex.order_by(rows, [("city", "ASC"), ("total", "DESC")])
        self.assertEqual(got, sorted(rows, key=lambda r: (r["city"], -r["total"])))
        top = ex.order_by(rows, [("city", "DESC"), ("total", "ASC")], limit=5)
        full = ex.order_by(rows, [("city", "DESC"), ("total", "ASC")])
        self.assertEqual([(r["city"], r["total"]) for r in top], [(r["city"], r["total"]) for r in full[:5]])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.runs_needed(10**12, 10**9), 1000)
        rng = random.Random(3)
        for _ in range(100):
            streams = [sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 5))]
            self.assertEqual(list(sol.merge_sorted_streams(*streams)), sorted(x for s in streams for x in s))
        self.assertEqual(list(sol.dedupe_sorted_stream([1, 1, 2, 3, 3, 3, 5])), [1, 2, 3, 5])
        self.assertEqual(sol.top_k_streaming(range(1000), 3), [999, 998, 997])


if __name__ == "__main__":
    unittest.main()
