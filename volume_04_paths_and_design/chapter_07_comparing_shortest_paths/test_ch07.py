import unittest

import ch07_examples as ex


class TestChapter7(unittest.TestCase):
    def test_town(self) -> None:
        self.assertEqual(set(ex.town_answers().values()), {15})

    def test_every_case(self) -> None:
        self.assertEqual(set(ex.one_source(300, 900)), {"Dijkstra", "Bellman-Ford"})     # answers asserted inside
        self.assertEqual(set(ex.all_pairs(40, 120)), {"Dijkstra from every place", "Floyd-Warshall"})
        adj, edges = ex.random_map(500, 1500)
        log = []
        ex.bf.bellman_ford(list(range(500)), edges, 0, log)
        self.assertLess(len(log), 30)
        p = [str(i) for i in range(200)]
        chain = [(str(i), str(i + 1), 1) for i in range(199)][::-1]
        log = []
        self.assertEqual(ex.bf.bellman_ford(p, chain, "0", log)[0]["199"], 199)
        self.assertEqual(len(log), 199)
        neg = {"A": {"B": 5, "C": 2}, "B": {"C": -4}, "C": {"D": 1}, "D": {}}
        edges = [(a, b, w) for a in neg for b, w in neg[a].items()]
        self.assertEqual((ex.dij.dijkstra(neg, "A")[0]["D"], ex.bf.bellman_ford(list(neg), edges, "A")[0]["D"]), (3, 2))


if __name__ == "__main__":
    unittest.main()
