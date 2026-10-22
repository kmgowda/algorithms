import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


def brute_widest(adj, s):
    best = {s: float("inf")}
    changed = True
    while changed:
        changed = False
        for v in list(best):
            for w, lim in adj[v].items():
                if min(best[v], lim) > best.get(w, float("-inf")):
                    best[w] = min(best[v], lim)
                    changed = True
    return best


class TestChapter2Solutions(unittest.TestCase):
    def test_widest_smallest(self) -> None:
        self.assertEqual(sol.widest_routes({"A": {}}, "A")[0], {"A": float("inf")})
        w, p = sol.widest_routes({"A": {"B": 4}, "B": {"A": 4}, "C": {}}, "A")
        self.assertEqual((w, "C" in w, p["B"]), ({"A": float("inf"), "B": 4}, False, "A"))

    def test_widest_prefers_wide_detour(self) -> None:
        adj = ex.weighted_adjacency(["A", "B", "C"], [("A", "C", 2), ("A", "B", 7), ("B", "C", 5)])
        w, p = sol.widest_routes(adj, "A")
        self.assertEqual((w["C"], ex.route(p, "C")), (5, ["A", "B", "C"]))

    def test_widest_random(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            n = rng.randint(1, 7)
            adj = {i: {} for i in range(n)}
            for _ in range(rng.randint(0, 12)):
                a, b = rng.randrange(n), rng.randrange(n)
                if a != b:
                    adj[a][b] = adj[b][a] = rng.randint(1, 9)
            self.assertEqual(sol.widest_routes(adj, 0)[0], brute_widest(adj, 0))

    def test_meeting_rule(self) -> None:
        tri = {"S": {"A": 3, "T": 5}, "A": {"S": 3, "T": 3}, "T": {"S": 5, "A": 3}}
        self.assertEqual(sol.meet_first_settled_twice(tri, "S", "T"), (6, "A"))      # wrong: the road S-T is 5
        self.assertEqual(sol.meet_in_middle(tri, "S", "T"), 5)
        self.assertEqual(sol.meet_in_middle({"A": {}}, "A", "A"), 0)
        self.assertIsNone(sol.meet_in_middle({"A": {}, "B": {}}, "A", "B"))
        rng = random.Random(3)
        for _ in range(300):
            n = rng.randint(2, 7)
            adj = {i: {} for i in range(n)}
            for _ in range(rng.randint(0, 12)):
                a, b = rng.randrange(n), rng.randrange(n)
                if a != b:
                    adj[a][b] = adj[b][a] = rng.randint(1, 9)
            self.assertEqual(sol.meet_in_middle(adj, 0, n - 1), ex.dijkstra(adj, 0)[0].get(n - 1))


if __name__ == "__main__":
    unittest.main()
