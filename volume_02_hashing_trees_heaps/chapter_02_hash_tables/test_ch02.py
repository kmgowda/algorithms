import random
import unittest

import ch02_examples as ex


class TestChapter31(unittest.TestCase):
    def test_every_case(self) -> None:
        c = ex.ChainedTable(8)
        for k in (1, 9, 17):
            c.put(k, str(k))
        self.assertEqual([k for k, _ in c.slots[1]], [1, 9, 17])
        self.assertEqual((c.get(9), c.get(25), c.delete(25)), ("9", None, False))
        self.assertTrue(c.delete(9))
        self.assertEqual((c.get(9), c.get(17)), (None, "17"))
        c.put(1, "one")
        self.assertEqual((c.get(1), c.size), ("one", 2))
        d = ex.ChainedTable(8)
        for k in range(6):
            d.put(k, k)
        self.assertEqual(len(d.slots), 8)
        d.put(6, 6)
        self.assertEqual((len(d.slots), d.get(3)), (16, 3))
        p = ex.ProbingTable(8)
        for k in (1, 9, 17):
            p.put(k, str(k))
        self.assertEqual(p.keys[1:4], [1, 9, 17])
        p.delete(9)
        self.assertIs(p.keys[2], ex._TOMB)
        self.assertEqual((p.get(17), p.get(9)), ("17", None))
        p.put(25, "25")
        self.assertEqual(p.keys[2], 25)
        self.assertEqual((ex.ProbingTable().get("x", "none"), ex.ProbingTable().delete("x")), ("none", False))
        q = ex.ProbingTable(8)
        for k in range(5):
            q.put(k, k)
        self.assertEqual(len(q.keys), 8)
        q.put(5, 5)
        self.assertEqual((len(q.keys), q.get(4)), (16, 4))

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
        self.assertAlmostEqual(ex.failed_search_probes(0.5, searches=2000), 2.5, delta=0.2)

    def test_probe_sequences(self) -> None:
        self.assertEqual(list(ex.probe_sequence(35, 16, "linear"))[:4], [3, 4, 5, 6])
        self.assertEqual(list(ex.probe_sequence(35, 16, "quadratic"))[:4], [3, 4, 6, 9])
        self.assertEqual(list(ex.probe_sequence(35, 16, "double"))[:4], [3, 6, 9, 12])
        self.assertEqual(list(ex.probe_sequence(67, 16, "double"))[:4], [3, 8, 13, 2])
        for mode in ("linear", "quadratic", "double"):
            for k in (0, 1, 35, 67, 1000):
                self.assertEqual(sorted(ex.probe_sequence(k, 16, mode)), list(range(16)))   # every slot reached
            self.assertEqual(list(ex.probe_sequence(5, 1, mode)), [0])                      # one slot

    def test_other_probing_tables(self) -> None:
        rng = random.Random(2)
        for mode in ("quadratic", "double"):
            t, ref = ex.ProbingTable(8, mode), {}
            self.assertEqual((t.get(1), t.delete(1)), (None, False))
            for _ in range(4000):
                k = rng.randint(0, 200)
                if rng.random() < 0.6:
                    t.put(k, k * 2)
                    ref[k] = k * 2
                else:
                    self.assertEqual(t.delete(k), k in ref)
                    ref.pop(k, None)
            for k in range(201):
                self.assertEqual(t.get(k), ref.get(k))

    def test_clustering_experiment(self) -> None:
        lin, quad, dbl = (ex.failed_search_probes(0.75, mode, searches=1000) for mode in ("linear", "quadratic", "double"))
        self.assertGreater(lin, quad)
        self.assertGreater(quad, dbl)
        self.assertAlmostEqual(dbl, 4.0, delta=0.6)          # uniform hashing: 1 / (1 - 0.75)
        self.assertEqual(ex.failed_search_probes(0.0), 1.0)  # an empty table: one look

    def test_hash_design(self) -> None:
        calls = [100 + 8 * j for j in range(7)]
        self.assertEqual({ex.division_hash(k, 8) for k in calls}, {4})
        self.assertEqual(sorted(ex.division_hash(k, 7) for k in calls), list(range(7)))
        self.assertEqual(ex.multiplication_hash(100, 8), 6)
        self.assertEqual(ex.multiplication_hash(0, 8), 0)
        attack = [16 * j for j in range(50)]
        self.assertEqual(ex.longest_chain(attack, 16, lambda k: k % 16), 50)
        self.assertEqual(ex.longest_chain(attack, 16, ex.random_universal_hash(16, random.Random(7))), 5)
        self.assertEqual(ex.longest_chain([], 16, lambda k: 0), 0)
        self.assertLess(ex.collision_rate(100, 116, 16), 1 / 16 + 0.01)
        h = ex.random_universal_hash(1, random.Random(1))
        self.assertEqual(h(12345), 0)                        # one slot: everything collides


if __name__ == "__main__":
    unittest.main()
