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


    def test_bidirectional(self) -> None:
        self.assertEqual(ex.bidirectional(ex.TRICK, "S", "T"), (9, 4, "B"))
        self.assertEqual(ex.bidirectional(ex.TRICK, "S", "T", naive=True), (10, 6, "U"))      # wrong: 10, not 9
        adj = ex.dij.weighted_adjacency()
        self.assertEqual(ex.bidirectional(adj, "Library", "Harbour")[0], 15)
        self.assertEqual(ex.bidirectional(adj, "Library", "Library"), (0, 1, "Library"))
        self.assertEqual(ex.bidirectional({"A": {}, "B": {}}, "A", "B")[0], float("inf"))
        self.assertEqual(ex.bidirectional({"A": {"B": 2}, "B": {"A": 2}}, "A", "B")[0], 2)
        one, two = ex.one_vs_two_ends(2000, 6000, trials=10)                                  # answers asserted inside
        self.assertLess(two, one)
        self.assertEqual((ex.one_vs_two_ends(10000, 30000), ex.one_vs_two_ends(0, 0, grid=100)),
                         ((2591, 107), (5339, 3671)))                                          # Figure 7.2
        self.assertEqual(ex.inflated_guess(), [(1, 61, 669), (2, 61, 338), (5, 61, 222)])
        one, two = ex.one_vs_two_ends(0, 0, trials=10, grid=30)
        self.assertLess(two, one)


if __name__ == "__main__":
    unittest.main()
