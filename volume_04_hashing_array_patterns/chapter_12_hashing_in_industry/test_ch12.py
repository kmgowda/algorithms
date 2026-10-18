import unittest

import ch12_examples as ex
import ch12_solutions as sol

KEYS = [f"user{i}" for i in range(5000)]
SERVERS = ["db-a", "db-b", "db-c", "db-d"]


class TestSharding(unittest.TestCase):
    def test_stable_hash(self) -> None:
        self.assertEqual(ex.stable_hash("lion"), ex.stable_hash("lion"))
        self.assertNotEqual(ex.stable_hash("lion"), ex.stable_hash("lioN"))

    def test_mod_moves_most_keys(self) -> None:
        self.assertGreater(ex.moved_fraction_mod(KEYS, 4, 5), 0.7)

    def test_ring_moves_few_keys(self) -> None:
        moved = ex.moved_fraction_ring(KEYS, SERVERS, "db-e")
        self.assertLess(moved, 0.3)
        self.assertGreater(moved, 0.1)

    def test_ring_balance_and_wrap(self) -> None:
        ring = ex.ConsistentHashRing(SERVERS)
        spread = ex.load_spread(KEYS, ring)
        self.assertEqual(set(spread), set(SERVERS))
        self.assertLess(max(spread.values()) / min(spread.values()), 1.6)
        with self.assertRaises(LookupError):
            ex.ConsistentHashRing([]).server_for("x")
        self.assertEqual(ex.ConsistentHashRing(["only"]).server_for("anything"), "only")


class TestBloom(unittest.TestCase):
    def test_no_false_negatives_and_low_false_positives(self) -> None:
        b = ex.BloomFilter(20_000, 4)
        for k in KEYS[:2000]:
            b.add(k)
        self.assertTrue(all(b.might_contain(k) for k in KEYS[:2000]))
        fp = sum(b.might_contain(f"stranger{i}") for i in range(3000)) / 3000
        expected = sol.bloom_false_positive_rate(20_000, 4, 2000)
        self.assertLess(abs(fp - expected), 0.03)


class TestSolutions(unittest.TestCase):
    def test_rendezvous(self) -> None:
        before = {k: sol.rendezvous_server(k, SERVERS) for k in KEYS}
        after = {k: sol.rendezvous_server(k, SERVERS + ["db-e"]) for k in KEYS}
        moved = [k for k in KEYS if before[k] != after[k]]
        self.assertTrue(all(after[k] == "db-e" for k in moved))
        self.assertLess(len(moved) / len(KEYS), 0.3)

    def test_formulas(self) -> None:
        self.assertAlmostEqual(sol.bloom_false_positive_rate(20_000, 4, 2000), 0.0118, places=3)
        self.assertEqual(sol.best_hash_count(20_000, 2000), 7)

    def test_removal(self) -> None:
        moved, only_its = sol.keys_moved_on_removal(KEYS[:1000], ["a", "b", "c"], "b")
        self.assertTrue(only_its)
        self.assertGreater(moved, 0)


if __name__ == "__main__":
    unittest.main()
