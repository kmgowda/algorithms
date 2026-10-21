import random
import unittest

import ch02_examples as ex


class TestChapter31(unittest.TestCase):
    def test_tables_against_dict(self) -> None:
        rng = random.Random(1)
        for cls in (ex.ChainedTable, ex.ProbingTable):
            t, ref = cls(), {}
            for _ in range(5000):
                k = rng.randint(0, 300)
                op = rng.random()
                if op < 0.5:
                    t.put(k, op)
                    ref[k] = op
                elif op < 0.75:
                    self.assertEqual(t.delete(k), k in ref)
                    ref.pop(k, None)
                else:
                    self.assertEqual(t.get(k), ref.get(k))
            for k in range(301):
                self.assertEqual(t.get(k), ref.get(k))

    def test_tombstone_keeps_search_working(self) -> None:
        t = ex.ProbingTable(64)
        keys = [0, 64, 128]                  # all hash to slot 0 in a 64-slot table
        for k in keys:
            t.put(k, k)
        t.delete(64)
        self.assertEqual(t.get(128), 128)

    def test_probe_experiment(self) -> None:
        self.assertAlmostEqual(ex.failed_search_probes(0.5, searches=2000), 2.5, delta=0.4)


if __name__ == "__main__":
    unittest.main()
