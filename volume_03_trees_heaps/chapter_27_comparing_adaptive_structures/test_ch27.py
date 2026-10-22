import unittest

import ch27_examples as ex


class TestChapter27(unittest.TestCase):
    def test_sorted_load(self) -> None:
        h = {name: height for name, (shape, height) in ex.sorted_load_shapes().items()}
        self.assertEqual(h, {"plain BST": 8, "red-black": 3, "splay": 8, "treap": 3})
        self.assertEqual(ex.sorted_heights(), {"red-black": 16, "splay": 999, "treap": 20})

    def test_cost_strips(self) -> None:
        s = ex.cost_strips()
        self.assertEqual(s["red-black"], [3, 3, 3, 4, 1, 1, 1, 1, 2, 3])
        self.assertEqual(s["splay"], [9, 1, 1, 3, 5, 1, 1, 1, 3, 3])
        self.assertEqual(s["treap"], [3, 3, 3, 4, 3, 3, 3, 3, 3, 3])
        self.assertEqual([sum(v) for v in s.values()], [22, 28, 31])

    def test_workloads(self) -> None:
        w = ex.workloads(2000, 4000)
        self.assertLess(w["hot"]["splay"], w["hot"]["red-black"])
        self.assertLess(w["sequential"]["splay"], w["sequential"]["red-black"])
        self.assertLess(w["uniform"]["red-black"], w["uniform"]["splay"])
        w = ex.workloads()
        rounded = {p: {t: round(v, 2) for t, v in row.items()} for p, row in w.items()}
        self.assertEqual(rounded["uniform"], {"red-black": 12.62, "splay": 17.22, "treap": 16.4})
        self.assertEqual(rounded["hot"], {"red-black": 12.35, "splay": 5.22, "treap": 16.95})
        self.assertEqual(rounded["sequential"], {"red-black": 12.64, "splay": 3.55, "treap": 16.41})

    def test_hot_split(self) -> None:
        (hot, nh), (cold, nc) = ex.hot_split()
        self.assertEqual((nh, nc), (17947, 2053))
        self.assertEqual((round(hot, 2), round(cold, 2)), (3.86, 17.07))
        self.assertAlmostEqual((hot * nh + cold * nc) / 20000, ex.workloads()["hot"]["splay"])

    def test_edge_cases(self) -> None:
        e = ex.edge_cases()
        self.assertTrue(all(e["empty: search 5"].values()))
        self.assertEqual(set(e["one key: search it"].values()), {1})
        self.assertEqual(e["sorted load of 5, search 1"], {"red-black": 2, "splay": 5, "treap": 2})
        self.assertEqual(e["then search 1 again"], {"red-black": 2, "splay": 1, "treap": 2})

    def test_fib_spike(self) -> None:
        self.assertEqual(ex.fib_insert_then_delete_min(1024), (1013, 10))
        self.assertEqual(ex.fib_insert_then_delete_min(1), (0, 0))
        self.assertEqual(ex.fib_insert_then_delete_min(2), (0, 1))

    def test_depth_of(self) -> None:
        t = ex.tr.shelf_treap()
        self.assertEqual(ex.depth_of(t.root, 58), 0)
        with self.assertRaises(KeyError):
            ex.depth_of(t.root, 50)


if __name__ == "__main__":
    unittest.main()
