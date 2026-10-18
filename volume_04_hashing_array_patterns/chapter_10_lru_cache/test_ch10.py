import random
import unittest
from collections import OrderedDict

import ch10_examples as ex
import ch10_solutions as sol


class ModelLRU:
    def __init__(self, cap):
        self.cap, self.d = cap, OrderedDict()

    def get(self, k):
        if k not in self.d:
            return None
        self.d.move_to_end(k)
        return self.d[k]

    def put(self, k, v):
        self.d[k] = v
        self.d.move_to_end(k)
        if len(self.d) > self.cap:
            self.d.popitem(last=False)


class TestLRU(unittest.TestCase):
    def test_against_model(self) -> None:
        rng = random.Random(1)
        for cap in (1, 2, 3, 5):
            for cls in (ex.LRUCache, ex.OrderedDictLRU):
                cache, model = cls(cap), ModelLRU(cap)
                for _ in range(2000):
                    k = rng.randint(0, 7)
                    if rng.random() < 0.5:
                        v = rng.randint(0, 99)
                        cache.put(k, v)
                        model.put(k, v)
                    else:
                        self.assertEqual(cache.get(k), model.get(k))
                if cls is ex.LRUCache:
                    self.assertEqual(cache.keys_most_recent_first(), list(reversed(model.d)))
                    self.assertLessEqual(len(cache), cap)

    def test_example_and_errors(self) -> None:
        c = ex.LRUCache(2)
        c.put("lion", 1)
        c.put("panda", 2)
        c.get("lion")
        c.put("koala", 3)
        self.assertIsNone(c.get("panda"))
        self.assertEqual(c.keys_most_recent_first(), ["koala", "lion"])
        with self.assertRaises(ValueError):
            ex.LRUCache(0)

    def test_cached_lookup_and_hit_rate(self) -> None:
        calls = []
        f = ex.cached_lookup(lambda u: calls.append(u) or u.upper(), 2)
        for u in ["maya", "leo", "maya", "zoe", "maya", "leo"]:
            self.assertEqual(f(u), u.upper())
        self.assertEqual(calls, ["maya", "leo", "zoe", "leo"])
        trace = ["home", "news", "home", "maps", "home", "news", "mail", "home", "news", "maps"]
        rates = [ex.hit_rate(trace, c) for c in (1, 2, 3, 4)]
        self.assertEqual(rates, sorted(rates))
        self.assertEqual(ex.hit_rate([], 2), 0.0)


class TestSolutions(unittest.TestCase):
    def test_ttl(self) -> None:
        t = sol.TTLCache(10)
        t.put("w", "sunny", now=0)
        self.assertEqual(t.get("w", now=5), "sunny")
        self.assertIsNone(t.get("w", now=10))

    def test_byte_budget(self) -> None:
        b = sol.ByteBudgetLRU(10)
        b.put("a", b"12345")
        b.put("b", b"123456")
        self.assertIsNone(b.get("a"))
        self.assertEqual(b.get("b"), b"123456")
        b.put("huge", b"x" * 20)
        self.assertIsNone(b.get("huge"))
        self.assertLessEqual(b.used, 10)

    def test_fifo_vs_lru(self) -> None:
        self.assertEqual(sol.fifo_vs_lru_misses(["a", "b", "a", "c", "a", "d", "a"], 2), (5, 4))


if __name__ == "__main__":
    unittest.main()
