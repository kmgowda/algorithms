import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestHashMaps(unittest.TestCase):
    def run_model(self, cls) -> None:
        rng = random.Random(5)
        table, model = cls(), {}
        for _ in range(5000):
            op = rng.random()
            key = rng.randint(0, 300)
            if op < 0.5:
                value = rng.randint(0, 9)
                table[key] = value
                model[key] = value
            elif op < 0.75:
                if key in model:
                    del table[key]
                    del model[key]
                else:
                    with self.assertRaises(KeyError):
                        del table[key]
            else:
                self.assertEqual(key in table, key in model)
                if key in model:
                    self.assertEqual(table[key], model[key])
                else:
                    with self.assertRaises(KeyError):
                        table[key]
            self.assertEqual(len(table), len(model))
        self.assertEqual(sorted(table), sorted(model))

    def test_chaining(self) -> None:
        self.run_model(ex.ChainedHashMap)
        t = ex.ChainedHashMap(slots=2)
        for i in range(100):
            t[i] = i
        self.assertLessEqual(t.load_factor, ex.ChainedHashMap.MAX_LOAD)
        self.assertGreater(t.resizes, 0)
        self.assertEqual(t.get("missing", "none"), "none")

    def test_open_addressing(self) -> None:
        self.run_model(ex.OpenAddressingHashMap)

    def test_tombstones_keep_chains_intact(self) -> None:
        t = ex.OpenAddressingHashMap(slots=8)
        keys = [8, 16, 24]                      # small ints hash to themselves: all start at slot 0
        for k in keys:
            t[k] = k
        del t[16]
        self.assertEqual(t[24], 24)             # still found by probing past the tombstone
        t[16] = 99
        self.assertEqual(t[16], 99)

    def test_probes_stay_small(self) -> None:
        t = ex.OpenAddressingHashMap()
        for i in range(2000):
            t[f"k{i}"] = i
        t.probes = 0
        for i in range(2000):
            _ = t[f"k{i}"]
        self.assertLess(t.probes / 2000, 3)

    def test_stock(self) -> None:
        stock = ex.stock_levels([("MILK", 20), ("EGGS", 12), ("MILK", 5)])
        self.assertEqual((stock["MILK"], stock["EGGS"]), (25, 12))


class TestSolutions(unittest.TestCase):
    def test_hash_set(self) -> None:
        s = sol.HashSet()
        for x in (1, 2, 2, 3):
            s.add(x)
        s.remove(2)
        s.remove(99)
        self.assertEqual(len(s), 2)
        self.assertNotIn(2, s)

    def test_probe_estimates(self) -> None:
        self.assertEqual(sol.expected_probes_linear(0.5), (1.5, 2.5))
        self.assertGreater(sol.expected_probes_linear(0.9)[1], 40)
        with self.assertRaises(ValueError):
            sol.expected_probes_linear(1.0)

    def test_worst_case(self) -> None:
        self.assertEqual(sol.worst_case_chain(50), 50)


if __name__ == "__main__":
    unittest.main()
