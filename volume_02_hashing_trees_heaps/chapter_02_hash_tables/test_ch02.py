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
        self.assertAlmostEqual(ex.failed_search_probes(0.5, searches=2000), 2.5, delta=0.4)


if __name__ == "__main__":
    unittest.main()
