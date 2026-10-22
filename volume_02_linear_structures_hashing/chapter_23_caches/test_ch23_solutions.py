import random
import unittest

import ch23_examples as ex
import ch23_solutions as sol


class TestInclusion(unittest.TestCase):
    def test_belady_anomaly(self) -> None:
        reqs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
        self.assertEqual(sol.fifo_hits_by_size(reqs, (3, 4)), [3, 2])
        self.assertEqual([ex.count_hits(reqs, k) for k in (3, 4)], [2, 4])

    def test_lru_never_worse_with_more_room(self) -> None:
        rng = random.Random(23)
        for _ in range(300):
            reqs = [rng.randrange(6) for _ in range(rng.randint(0, 30))]
            hits = [ex.count_hits(reqs, k) for k in range(0, 8)]
            self.assertEqual(hits, sorted(hits))


class TestWidthLRU(unittest.TestCase):
    def test_smallest(self) -> None:
        self.assertEqual(sol.width_lru_hits([], {}, 10), (0, []))
        self.assertEqual(sol.width_lru_hits(["a", "a"], {"a": 11}, 10), (0, []))
        self.assertEqual(sol.width_lru_hits(["a", "a"], {"a": 10}, 10), (1, ["a"]))
        self.assertEqual(sol.width_lru_hits(["a"], {"a": 1}, 0), (0, []))

    def test_example(self) -> None:
        w = {"Atlas": 5, "Maps": 2, "Clocks": 2, "Stars": 3}
        reqs = ["Maps", "Clocks", "Stars", "Maps", "Atlas", "Maps", "Clocks"]
        self.assertEqual(sol.width_lru_hits(reqs, w, 8), (2, ["Maps", "Clocks"]))

    def test_equal_widths_match_lru(self) -> None:
        rng = random.Random(5)
        for _ in range(300):
            reqs = [rng.randrange(8) for _ in range(rng.randint(0, 40))]
            k = rng.randint(1, 5)
            self.assertEqual(sol.width_lru_hits(reqs, {i: 1 for i in range(8)}, k)[0], ex.count_hits(reqs, k))


class TestEvictFirstBug(unittest.TestCase):
    def test_counterexample(self) -> None:
        good, bad = ex.LRUCache(2), sol.EvictFirstLRU(2)
        for c in (good, bad):
            c.put("a", 1); c.put("b", 2); c.put("b", 3)
        self.assertEqual((good.keys_oldest_first(), good.get("a")), (["a", "b"], 1))
        self.assertEqual((bad.keys_oldest_first(), bad.get("a")), (["b"], None))


if __name__ == "__main__":
    unittest.main()
