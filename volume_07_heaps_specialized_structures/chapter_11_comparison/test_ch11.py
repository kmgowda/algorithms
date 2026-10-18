import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestComparison(unittest.TestCase):
    def test_compact_structures(self) -> None:
        rng = random.Random(1)
        vals = [rng.randint(0, 9) for _ in range(50)]
        f, s = ex.Fenwick(50), ex.SegSum(vals)
        for i, v in enumerate(vals):
            f.add(i, v)
        for _ in range(300):
            a, b = sorted((rng.randrange(50), rng.randrange(50)))
            self.assertEqual(f.prefix(b + 1) - f.prefix(a), sum(vals[a:b + 1]))
            self.assertEqual(s.total(a, b + 1), sum(vals[a:b + 1]))
            i, v = rng.randrange(50), rng.randint(0, 9)
            f.add(i, v - vals[i])
            s.set(i, v)
            vals[i] = v

    def test_races(self) -> None:
        r = ex.race_range_sums(5000, 2000)
        self.assertLess(r["Fenwick"], r["plain list"])
        self.assertEqual(set(ex.race_priority(2000)), {"heap", "sorted list"})

    def test_connectivity(self) -> None:
        rng = random.Random(2)
        for _ in range(10):
            edges = [(rng.randrange(30), rng.randrange(30)) for _ in range(40)]
            uf, bfs = ex.connected_after_each_edge(30, edges, 0, 1)
            self.assertEqual(uf, bfs)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        picks = sol.pick_for_scenarios()
        self.assertEqual(picks["hospital triage board"], "binary heap")
        self.assertEqual(picks["URL shortener: has this short code ever been used?"], "Bloom filter")
        mem = sol.memory_estimate(1024)
        self.assertLess(mem["Fenwick tree"], mem["segment tree (recursive)"])


if __name__ == "__main__":
    unittest.main()
