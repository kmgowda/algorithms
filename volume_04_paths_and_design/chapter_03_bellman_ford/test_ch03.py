import unittest

import ch03_examples as ex


class TestChapter3(unittest.TestCase):
    def test_courier(self) -> None:
        log = []
        dist, parent, cycle = ex.bellman_ford(ex.DEPOTS, ex.LEGS, "A", log)
        self.assertEqual(dist, {"A": 0, "B": 2, "C": 7, "D": 4, "E": -2})
        self.assertFalse(cycle)
        self.assertEqual(len(log), 3)
        self.assertEqual(log[0][1], {"A": 0, "B": 2, "C": 7, "D": 4, "E": 2})
        self.assertEqual(ex.route(parent, "E"), ["A", "C", "D", "B", "E"])

    def test_every_case(self) -> None:
        dist, _, cycle = ex.bellman_ford(["A", "B", "C"], [("A", "B", 1), ("B", "C", -3), ("C", "B", 1)], "A")
        self.assertTrue(cycle)
        self.assertEqual(ex.bellman_ford(["A", "B"], [], "A")[0], {"A": 0, "B": float("inf")})
        self.assertEqual(ex.bellman_ford(["A"], [], "A")[0], {"A": 0})
        p = [str(i) for i in range(6)]
        chain = [(str(i), str(i + 1), 1) for i in range(5)]
        slow, fast = [], []
        self.assertEqual(ex.bellman_ford(p, chain[::-1], "0", slow)[0]["5"], 5)
        ex.bellman_ford(p, chain, "0", fast)
        self.assertEqual((len(slow), len(fast)), (5, 2))
        zero = ex.bellman_ford(["A", "B"], [("A", "B", 0)], "A")[0]
        self.assertEqual(zero, {"A": 0, "B": 0})


if __name__ == "__main__":
    unittest.main()
