import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestStability(unittest.TestCase):
    def test_stable_check(self) -> None:
        pupils = [("Ana", "B"), ("Ben", "A"), ("Cy", "B"), ("Dev", "A")]
        self.assertTrue(ex.is_stable_result(pupils, sorted(pupils, key=lambda p: p[1]), key=lambda p: p[1]))
        bad = [pupils[3], pupils[1], pupils[0], pupils[2]]
        self.assertFalse(ex.is_stable_result(pupils, bad, key=lambda p: p[1]))

    def test_multi_column(self) -> None:
        rng = random.Random(1)
        rows = [{"city": rng.choice("ABC"), "name": rng.choice("xyz"), "id": i} for i in range(40)]
        self.assertEqual(ex.sort_by_columns(rows, ["city", "name"]), sorted(rows, key=lambda r: (r["city"], r["name"])))


class TestTimsort(unittest.TestCase):
    def test_runs_and_minrun(self) -> None:
        a = [1, 2, 3, 9, 8, 7, 4, 5, 6]
        self.assertEqual(ex.find_runs(a), [(0, 4), (4, 7), (7, 9)])     # 8 7 4 is one descending run
        self.assertEqual(a, [1, 2, 3, 9, 4, 7, 8, 5, 6])                 # ... reversed in place
        for n in (1, 63, 64, 65, 1000, 10**6):
            m = ex.min_run_length(n)
            self.assertTrue((n < 64 and m == n) or 32 <= m <= 64)

    def test_simple_timsort(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            n = rng.randint(0, 300)
            kind = rng.random()
            v = [rng.randint(0, 50) for _ in range(n)]
            if kind < 0.3:
                v.sort()
            elif kind < 0.5:
                v.sort(reverse=True)
            self.assertEqual(ex.simple_timsort(v), sorted(v))

    def test_timsort_stable(self) -> None:
        class Item:
            def __init__(self, k, i):
                self.k, self.i = k, i

            def __lt__(self, o):
                return self.k < o.k

            def __gt__(self, o):
                return self.k > o.k

            def __ge__(self, o):
                return self.k >= o.k

        rng = random.Random(3)
        items = [Item(rng.randint(0, 5), i) for i in range(200)]
        out = ex.simple_timsort(items)
        self.assertTrue(all((a.k, a.i) < (b.k, b.i) for a, b in zip(out, out[1:])))

    def test_shop(self) -> None:
        products = [{"name": "Mug A", "price": 5, "rating": 3.9}, {"name": "Mug B", "price": 5, "rating": 4.8},
                    {"name": "Cup", "price": 3, "rating": 4.1}]
        self.assertEqual(ex.shop_listing(products), ["Cup", "Mug B", "Mug A"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.stabilize([("x", 2), ("y", 1), ("z", 2)], key=lambda p: p[1]), [("y", 1), ("x", 2), ("z", 2)])
        self.assertEqual(sol.count_runs([1, 2, 5, 3, 4, 0]), 3)
        self.assertEqual(sol.count_runs([]), 0)
        self.assertEqual(sol.sort_emails([("Zoe", "hi", 1), ("Ali", "re", 2), ("Ben", "ok", 2)]),
                         [("Ali", "re", 2), ("Ben", "ok", 2), ("Zoe", "hi", 1)])


if __name__ == "__main__":
    unittest.main()
