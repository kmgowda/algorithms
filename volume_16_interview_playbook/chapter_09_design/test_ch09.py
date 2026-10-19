import random
import statistics
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestDesign(unittest.TestCase):
    def test_lru_against_model(self) -> None:
        rng = random.Random(1)
        for _ in range(30):
            cap = rng.randint(1, 4)
            cache, model = ex.LRUCache(cap), []          # model: list of (key, value), most recent last
            for _ in range(60):
                k = rng.randint(0, 6)
                if rng.random() < 0.5:
                    found = next((v for kk, v in model if kk == k), -1)
                    self.assertEqual(cache.get(k), found)
                    if found != -1:
                        model = [(kk, v) for kk, v in model if kk != k] + [(k, found)]
                else:
                    v = rng.randint(0, 99)
                    cache.put(k, v)
                    model = [(kk, vv) for kk, vv in model if kk != k] + [(k, v)]
                    model = model[-cap:]

    def test_others(self) -> None:
        rng = random.Random(2)
        data = [rng.randint(1, 9) for _ in range(20)]
        p = ex.PeekingIterator(iter(data))
        out = []
        while p.has_next():
            self.assertEqual(p.peek(), data[len(out)])
            out.append(p.next())
        self.assertEqual(out, data)
        tm = ex.TimeMap()
        history = []
        for t in range(1, 40, 3):
            v = str(rng.randint(0, 9))
            tm.set("k", v, t)
            history.append((t, v))
        for q in range(0, 45):
            expected = [v for t, v in history if t <= q]
            self.assertEqual(tm.get("k", q), expected[-1] if expected else "")
        rs, model = ex.RandomizedSet(rng), set()
        for _ in range(300):
            x = rng.randint(0, 15)
            if rng.random() < 0.5:
                self.assertEqual(rs.insert(x), x not in model)
                model.add(x)
            else:
                self.assertEqual(rs.remove(x), x in model)
                model.discard(x)
            self.assertEqual(sorted(rs.items), sorted(model))
            if model:
                self.assertIn(rs.get_random(), model)
        rl = ex.RateLimiter(3, 10)
        self.assertEqual([rl.allow("u1", t) for t in (0, 1, 2, 3, 11, 12)], [True, True, True, False, True, True])
        m, seen = sol.MedianFinder(), []
        for _ in range(50):
            x = rng.randint(-20, 20)
            m.add(x)
            seen.append(x)
            self.assertEqual(m.median(), statistics.median(seen))
        hc, log = sol.HitCounter(), []
        t = 0
        for _ in range(200):
            t += rng.randint(0, 40)
            hc.hit(t)
            log.append(t)
            self.assertEqual(hc.hits(t), sum(1 for x in log if t - x < 300))
        f = sol.Flatten2D([[1, 2], [], [3], []])
        got = []
        while f.has_next():
            got.append(f.next())
        self.assertEqual(got, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
