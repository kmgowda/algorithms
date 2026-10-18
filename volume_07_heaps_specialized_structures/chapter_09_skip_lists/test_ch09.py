import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestSkipList(unittest.TestCase):
    def test_against_dict(self) -> None:
        rng = random.Random(1)
        sl, model = ex.SkipList(seed=2), {}
        for _ in range(4000):
            k = rng.randint(0, 300)
            r = rng.random()
            if r < 0.5:
                sl.insert(k, -k)
                model[k] = -k
            elif r < 0.8:
                self.assertEqual(sl.delete(k), k in model)
                model.pop(k, None)
            else:
                self.assertEqual(k in sl, k in model)
        self.assertEqual(list(sl.keys()), sorted(model))
        self.assertEqual(sl.size, len(model))
        for k in list(model)[:30]:
            self.assertEqual(sl.get(k), model[k])
        with self.assertRaises(KeyError):
            sl.get(-1)
        self.assertEqual(sl.range(50, 120), [k for k in sorted(model) if 50 <= k <= 120])
        sizes = sl.lane_sizes()
        self.assertTrue(all(a >= b for a, b in zip(sizes, sizes[1:])))

    def test_leaderboard(self) -> None:
        self.assertEqual(ex.leaderboard({"Ana": 120, "Ben": 300, "Cy": 210}), ["Ben", "Cy", "Ana"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        small, big = sol.average_search_steps(1000), sol.average_search_steps(16000)
        self.assertLess(big, small * 3)
        self.assertLess(big, 40)
        sl = ex.SkipList(3)
        for k in (10, 20, 30):
            sl.insert(k)
        self.assertEqual((sol.floor_key(sl, 25), sol.floor_key(sl, 30), sol.floor_key(sl, 5)), (20, 30, None))
        self.assertEqual(sol.expected_pointers(10), 20.0)


if __name__ == "__main__":
    unittest.main()
