import random
import unittest

import ch17_examples as ex
import ch17_solutions as sol

TRAP = ex.adjacency(list("SABCDT"), [("S", "A"), ("S", "C"), ("A", "B"), ("B", "D"), ("C", "D"), ("D", "T")])


class TestChapter17Solutions(unittest.TestCase):
    def test_on_shortest_routes(self) -> None:
        adj = ex.adjacency()
        self.assertEqual(sol.on_shortest_routes(adj, "Library", "Museum"), set(ex.PLACES) - {"Harbour"})
        self.assertEqual(sol.on_shortest_routes(adj, "Library", "Harbour"),
                         {"Library", "School", "Station", "Harbour"})        # only one 3-road route
        self.assertEqual(sol.on_shortest_routes(adj, "Library", "Park"), {"Library", "Park"})
        self.assertEqual(sol.on_shortest_routes(adj, "Market", "Market"), {"Market"})
        self.assertEqual(sol.on_shortest_routes({"A": []}, "A", "A"), {"A"})
        island = ex.adjacency(ex.PLACES + ["Island"], ex.ROADS)
        self.assertEqual(sol.on_shortest_routes(island, "Library", "Island"), set())

    def test_brute_force(self) -> None:
        random.seed(7)
        for _ in range(300):
            n = random.randint(1, 7)
            roads = [(i, j) for i in range(n) for j in range(i + 1, n) if random.random() < 0.4]
            adj = ex.adjacency(list(range(n)), roads)
            a, b = random.randrange(n), random.randrange(n)
            da = ex.bfs(adj, a)[0]
            expected = set()
            if b in da:
                for w in adj:
                    dw = ex.bfs(adj, w)[0]
                    if w in da and b in dw and da[w] + dw[b] == da[b]:
                        expected.add(w)
            self.assertEqual(sol.on_shortest_routes(adj, a, b), expected)

    def test_meet_in_middle(self) -> None:
        self.assertEqual(sol.meet_in_middle_wrong(TRAP, "S", "T"), 4)     # the trap: one road too many
        self.assertEqual(sol.meet_in_middle(TRAP, "S", "T"), 3)
        self.assertEqual(ex.bfs(TRAP, "S")[0]["T"], 3)
        self.assertEqual(sol.meet_in_middle({"A": []}, "A", "A"), 0)
        self.assertIsNone(sol.meet_in_middle({"A": [], "B": []}, "A", "B"))
        self.assertIsNone(sol.meet_in_middle_wrong({"A": [], "B": []}, "A", "B"))
        random.seed(1)                                   # the flawed one is rarely wrong: 12 of 20,000 maps
        wrong = 0
        for _ in range(20000):
            n = random.randint(1, 9)
            p = random.random()
            roads = [(i, j) for i in range(n) for j in range(i + 1, n) if random.random() < p]
            adj = ex.adjacency(list(range(n)), roads)
            a, b = random.randrange(n), random.randrange(n)
            wrong += sol.meet_in_middle_wrong(adj, a, b) != ex.bfs(adj, a)[0].get(b)
        self.assertEqual(wrong, 12)
        random.seed(3)
        for _ in range(3000):
            n = random.randint(1, 9)
            p = random.random()
            roads = [(i, j) for i in range(n) for j in range(i + 1, n) if random.random() < p]
            adj = ex.adjacency(list(range(n)), roads)
            a, b = random.randrange(n), random.randrange(n)
            self.assertEqual(sol.meet_in_middle(adj, a, b), ex.bfs(adj, a)[0].get(b))


if __name__ == "__main__":
    unittest.main()
