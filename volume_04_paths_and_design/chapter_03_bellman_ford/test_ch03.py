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

    def test_cycles_spfa_and_legs(self) -> None:
        _, parent, _ = ex.bellman_ford(ex.DEPOTS, ex.LEGS, "A")
        self.assertEqual(ex.cheapest_leg_counts(parent, "A"), {"A": 0, "B": 3, "C": 1, "D": 2, "E": 4})
        backwards = []
        ex.bellman_ford(ex.DEPOTS, ex.LEGS[::-1], "A", backwards)
        self.assertEqual([r[1] for r in backwards[:3]], [{"A": 0, "B": 6, "C": 7, "D": float("inf"), "E": float("inf")},
                                                        {"A": 0, "B": 6, "C": 7, "D": 4, "E": 2},
                                                        {"A": 0, "B": 2, "C": 7, "D": 4, "E": -2}])
        self.assertEqual(len(backwards), 4)
        bonus = [leg if leg[:2] != ("E", "A") else ("E", "A", -3) for leg in ex.LEGS]
        self.assertEqual(ex.find_negative_cycle(ex.DEPOTS, bonus), ["C", "D", "B", "E", "A"])
        self.assertIsNone(ex.find_negative_cycle(ex.DEPOTS, ex.LEGS))
        self.assertEqual(ex.find_negative_cycle(["A", "B", "C"], [("A", "B", 1), ("B", "C", -3), ("C", "B", 1)]),
                         ["B", "C"])
        self.assertIsNone(ex.find_negative_cycle([], []))
        self.assertEqual(ex.find_negative_cycle(["A"], [("A", "A", -1)]), ["A"])
        self.assertEqual(ex.spfa(ex.DEPOTS, ex.LEGS, "A"), (ex.bellman_ford(ex.DEPOTS, ex.LEGS, "A")[0], 15))
        p = [str(i) for i in range(6)]
        chain = [(str(i), str(i + 1), 1) for i in range(5)]
        self.assertEqual(ex.spfa(p, chain[::-1], "0")[1], 5)
        self.assertEqual(ex.spfa(["A"], [], "A"), ({"A": 0}, 0))
        self.assertEqual(ex.bellman_ford(ex.DEPOTS, bonus, "A")[0]["A"], -10)
        steep = [leg if leg[:2] != ("D", "B") else ("D", "B", -6) for leg in ex.LEGS]
        self.assertIsNotNone(ex.find_negative_cycle(ex.DEPOTS, steep))
        self.assertEqual(ex.cheapest_within(ex.DEPOTS, ex.LEGS, "A", 2), {"A": 0, "B": 6, "C": 7, "D": 4, "E": 2})
        self.assertEqual(ex.cheapest_within(ex.DEPOTS, ex.LEGS, "A", 0)["B"], float("inf"))
        self.assertEqual(ex.cheapest_within(ex.DEPOTS, ex.LEGS, "A", 4), ex.bellman_ford(ex.DEPOTS, ex.LEGS, "A")[0])

if __name__ == "__main__":
    unittest.main()
