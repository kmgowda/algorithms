import itertools
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol

INF = float("inf")


def brute_cycle(n, edges):
    w = {}
    for a, b, c in edges:
        w[(a, b)] = min(w.get((a, b), INF), c)
    best = INF
    for r in range(1, n + 1):
        for cyc in itertools.permutations(range(n), r):
            legs = list(zip(cyc, cyc[1:] + cyc[:1]))
            if all(leg in w for leg in legs):
                best = min(best, sum(w[leg] for leg in legs))
    return best


class TestChapter5Solutions(unittest.TestCase):
    def test_courier(self) -> None:
        idx = {v: i for i, v in enumerate(ex.DEPOTS)}
        cost, cyc = sol.cheapest_round_trip(5, [(idx[a], idx[b], w) for a, b, w in ex.LEGS])
        self.assertEqual((cost, [ex.DEPOTS[i] for i in cyc]), (0, ["A", "C", "D", "B", "E", "A"]))

    def test_smallest(self) -> None:
        self.assertEqual(sol.cheapest_round_trip(0, []), (INF, None))
        self.assertEqual(sol.cheapest_round_trip(1, []), (INF, None))
        self.assertEqual(sol.cheapest_round_trip(1, [(0, 0, 2)]), (2, [0, 0]))
        self.assertEqual(sol.cheapest_round_trip(2, [(0, 1, 3)]), (INF, None))
        self.assertEqual(sol.cheapest_round_trip(2, [(0, 1, 3), (1, 0, 4)]), (7, [0, 1, 0]))

    def test_random(self) -> None:
        rng = random.Random(6)
        for _ in range(300):
            n = rng.randint(1, 5)
            edges = [(rng.randrange(n), rng.randrange(n), rng.randint(1, 9)) for _ in range(rng.randint(0, 9))]
            cost, cyc = sol.cheapest_round_trip(n, edges)
            self.assertEqual(cost, brute_cycle(n, edges))
            if cyc:
                w = {}
                for a, b, c in edges:
                    w[(a, b)] = min(w.get((a, b), INF), c)
                self.assertEqual(sum(w[(a, b)] for a, b in zip(cyc, cyc[1:])), cost)

    def test_k_innermost_is_wrong(self) -> None:
        chain = [(0, 2, 4), (2, 3, 4), (3, 1, 5)]
        self.assertEqual(sol.floyd_k_innermost(4, chain)[0][1], INF)
        self.assertEqual(ex.floyd_warshall(4, chain, directed=True)[0][0][1], 13)


if __name__ == "__main__":
    unittest.main()
