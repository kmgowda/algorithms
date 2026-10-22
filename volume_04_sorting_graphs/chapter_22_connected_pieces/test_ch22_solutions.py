import random
import unittest

import ch22_examples as ex
import ch22_solutions as sol


def brute_depots(g):
    return [v for v in g if len(sol.reach(g, v)) == len(g)]


class TestChapter22Solutions(unittest.TestCase):
    def test_town(self) -> None:
        self.assertEqual(sol.depots(ex.directed()), ["Library", "School", "Park", "Market"])
        self.assertEqual(sol.depots(ex.directed(arrows=[a for a in ex.ONE_WAY if a != ("Park", "Hospital")])), [])
        merged = ex.directed(arrows=ex.ONE_WAY + [("Museum", "Market")])
        self.assertEqual(sol.depots(merged), ex.PLACES)

    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.depots({}), [])
        self.assertEqual(sol.depots({"A": []}), ["A"])
        self.assertEqual(sol.depots({"A": ["A"]}), ["A"])
        self.assertEqual(sol.depots({"A": [], "B": []}), [])
        self.assertEqual(sol.depots({"A": ["B"], "B": []}), ["A"])

    def test_against_brute_force(self) -> None:
        rng = random.Random(22)
        for _ in range(500):
            n = rng.randint(1, 8)
            g = {v: [w for w in range(n) if rng.random() < 0.25] for v in range(n)}
            self.assertEqual(sol.depots(g), brute_depots(g), g)

    def test_smallest_finish_not_in_sink(self) -> None:
        g = {"Library": ["School", "Park"], "School": ["Library"], "Park": []}
        t = ex.finish_times(g)
        self.assertEqual(t, {"Library": (1, 6), "School": (2, 3), "Park": (4, 5)})
        self.assertEqual(min(g, key=lambda v: t[v][1]), "School")
        self.assertEqual(sorted(map(sorted, ex.strongly_connected(g))), [["Library", "School"], ["Park"]])

    def test_flawed_tarjan(self) -> None:
        g = {"Library": ["Park", "School"], "Park": [], "School": ["Park"]}
        self.assertEqual(sol.tarjan_any_visited(g), [["Park"], ["School", "Library"]])
        self.assertEqual(ex.tarjan_scc(g), [["Park"], ["School"], ["Library"]])
        self.assertEqual(sol.tarjan_any_visited(ex.directed()), ex.tarjan_scc(ex.directed()))


if __name__ == "__main__":
    unittest.main()
