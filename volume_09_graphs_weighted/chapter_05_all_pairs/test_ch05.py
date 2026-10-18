import heapq
import math
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


def bellman(n, edges, s):
    d = [math.inf] * n
    d[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return d


def has_neg(n, edges):
    d = [0] * n
    for _ in range(n):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return any(d[u] + w < d[v] for u, v, w in edges)


class TestAllPairs(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            n = rng.randint(1, 7)
            edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-3, 9)) for _ in range(rng.randint(0, 14))]
            edges = [e for e in edges if e[0] != e[1]]
            neg = has_neg(n, edges)
            self.assertEqual(sol.has_negative_cycle(n, edges), neg)
            j = ex.johnson(n, edges)
            if neg:
                self.assertIsNone(j)
                continue
            dist, nxt = ex.floyd_warshall(n, edges)
            for s in range(n):
                ref = bellman(n, edges, s)
                self.assertEqual(dist[s], ref)
                self.assertEqual(j[s], ref)
                for t in range(n):
                    p = ex.fw_path(nxt, s, t)
                    if ref[t] < math.inf:
                        best = {(u, v): min(w for a, b, w in edges if (a, b) == (u, v)) for u, v, _ in edges}
                        cost = sum(best[(a, b)] for a, b in zip(p, p[1:]))
                        self.assertEqual(cost, ref[t])
                    else:
                        self.assertEqual(p, [])

    def test_examples(self) -> None:
        cities = ["Pune", "Mumbai", "Nashik", "Surat"]
        roads = [("Pune", "Mumbai", 150), ("Mumbai", "Nashik", 170), ("Pune", "Nashik", 210), ("Mumbai", "Surat", 280)]
        self.assertEqual(ex.distance_table(cities, roads)["Pune"]["Surat"], 430)
        self.assertEqual(ex.best_meeting_city(cities, roads), "Mumbai")

    def test_solutions(self) -> None:
        self.assertEqual(sol.transitive_closure(3, [(0, 1), (1, 2)])[0][2], True)
        self.assertEqual(sol.transitive_closure(3, [(0, 1), (1, 2)])[2][0], False)
        self.assertEqual(sol.city_with_fewest_reachable(4, [(0, 1, 3), (1, 2, 1), (1, 3, 4), (2, 3, 1)], 4), 3)
        self.assertEqual(sol.diameter(3, [(0, 1, 2), (1, 2, 3)]), 5)


if __name__ == "__main__":
    unittest.main()
