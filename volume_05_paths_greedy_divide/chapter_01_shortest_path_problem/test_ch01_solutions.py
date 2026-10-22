import itertools
import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


def brute(adj, start, musts, goal, max_len=7):
    """Try every walk of up to max_len roads (small maps only)."""
    best = float("inf")
    frontier = [[start]]
    for _ in range(max_len + 1):
        nxt = []
        for w in frontier:
            if w[-1] == goal and set(musts) <= set(w):
                best = min(best, ex.route_length(adj, w))
            nxt.extend(w + [x] for x in adj[w[-1]])
        frontier = nxt
    return best


class TestChapter1Solutions(unittest.TestCase):
    def test_town(self) -> None:
        adj = ex.weighted_adjacency()
        self.assertEqual(sol.quickest_visiting_all(adj, "Library", ["Market", "School"], "Harbour")[0::2], (18, 32))
        self.assertEqual(sol.quickest_visiting_all(adj, "Library", ["Market"], "Harbour")[0],
                         ex.quickest_via(adj, "Library", "Market", "Harbour")[0])
        m, walk, n = sol.quickest_visiting_all(adj, "Library", ["Hospital", "School", "Station"], "Harbour")
        self.assertEqual((m, walk.count("Museum"), n), (27, 2, 64))      # a walk may repeat a place

    def test_smallest(self) -> None:
        self.assertEqual(sol.quickest_visiting_all({"A": {}}, "A", [], "A"), (0, ["A"], 1))
        self.assertEqual(sol.quickest_visiting_all({"A": {}}, "A", ["A"], "A")[0], 0)
        self.assertEqual(sol.quickest_visiting_all({"A": {}, "B": {}}, "A", [], "B")[:2], (float("inf"), None))

    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(60):
            n = rng.randint(2, 5)
            adj = {i: {} for i in range(n)}
            for a, b in itertools.combinations(range(n), 2):
                if rng.random() < 0.6:
                    adj[a][b] = adj[b][a] = rng.randint(1, 5)
            musts = rng.sample(range(n), rng.randint(0, min(2, n)))
            self.assertEqual(sol.quickest_visiting_all(adj, 0, musts, n - 1)[0], brute(adj, 0, musts, n - 1))


if __name__ == "__main__":
    unittest.main()
