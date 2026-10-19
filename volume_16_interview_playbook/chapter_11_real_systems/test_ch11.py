import itertools
import math
import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestRealSystems(unittest.TestCase):
    def test_routes_and_people(self) -> None:
        rng = random.Random(1)
        for _ in range(60):
            nodes = [f"n{i}" for i in range(rng.randint(2, 6))]
            roads = {u: [(v, rng.randint(1, 9)) for v in nodes if v != u and rng.random() < 0.5] for u in nodes}
            best = math.inf
            for r in range(len(nodes) - 1):
                for mid in itertools.permutations(nodes[1:-1], r):
                    path = [nodes[0], *mid, nodes[-1]]
                    cost = 0
                    for a, b in zip(path, path[1:]):
                        w = dict(roads[a]).get(b)
                        if w is None:
                            cost = math.inf
                            break
                        cost += w
                    best = min(best, cost)
            d, path = ex.fastest_route(roads, nodes[0], nodes[-1])
            self.assertEqual(d, best)
            if path:
                self.assertEqual(sum(dict(roads[a])[b] for a, b in zip(path, path[1:])), d)
            people = [f"p{i}" for i in range(rng.randint(2, 7))]
            fr = {p: set() for p in people}
            for a, b in itertools.combinations(people, 2):
                if rng.random() < 0.35:
                    fr[a].add(b)
                    fr[b].add(a)
            sugg = ex.friend_suggestions(fr, people[0], 10)
            for name, m in sugg:
                self.assertEqual(ex.degrees_of_separation(fr, people[0], name), 2)
                self.assertEqual(m, len(fr[people[0]] & fr[name]))
            comms = sol.connected_communities(fr)
            for g in comms:
                for a, b in itertools.combinations(g, 2):
                    self.assertNotEqual(ex.degrees_of_separation(fr, a, b), -1)

    def test_search_and_bank(self) -> None:
        idx = ex.SearchIndex({"a": "cheap flights to goa", "b": "goa beach hotels and goa food", "c": "cheap hotels in pune"})
        self.assertEqual(idx.search("goa hotels")[0][0], "b")
        self.assertEqual(sol.phrase_and(idx, "cheap hotels"), ["c"])
        self.assertEqual(sol.autocomplete({"goa trip": 50, "goa hotels": 80, "good food": 30, "pune": 10}, "go"),
                         ["goa hotels", "goa trip", "good food"])
        rng = random.Random(2)
        for _ in range(100):
            opening = {a: rng.randint(0, 100) for a in "ABC"}
            txs = [(rng.choice("ABC"), rng.choice("ABC"), rng.randint(-5, 80)) for _ in range(rng.randint(0, 8))]
            bal, rejected = ex.ledger(txs, opening)
            self.assertEqual(sum(bal.values()), sum(opening.values()))
            self.assertTrue(all(v >= 0 for v in bal.values()))
        self.assertEqual(ex.ledger([("A", "B", 50), ("B", "C", 80), ("A", "C", 60)], {"A": 100, "B": 40, "C": 0}),
                         ({"A": 50, "B": 10, "C": 80}, [2]))
        self.assertEqual(ex.fraud_flags([(0, "card1", "Pune"), (30, "card1", "Delhi"), (10, "card2", "Goa"), (500, "card2", "Pune")], 60), ["card1"])


if __name__ == "__main__":
    unittest.main()
