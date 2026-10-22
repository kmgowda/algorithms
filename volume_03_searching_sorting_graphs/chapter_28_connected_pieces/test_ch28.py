import unittest

import ch28_examples as ex


class TestChapter28(unittest.TestCase):
    def test_storm(self) -> None:
        roads = [r for r in ex.ROADS if r not in ex.CLOSED]
        self.assertEqual(len(roads), 5)
        self.assertEqual(ex.components(ex.adjacency(roads=roads)),
                         [["Library", "School", "Park"], ["Market", "Museum", "Hospital", "Station"], ["Harbour"]])
        self.assertEqual(len(ex.components(ex.adjacency(roads=roads + [("Station", "Harbour")]))), 2)

    def test_scc(self) -> None:
        groups = [sorted(g) for g in ex.strongly_connected(ex.directed())]
        self.assertEqual(groups, [["Library", "Market", "Park", "School"], ["Hospital"], ["Harbour", "Museum", "Station"]])
        merged = ex.strongly_connected(ex.directed(arrows=ex.ONE_WAY + [("Museum", "Market")]))
        self.assertEqual(len(merged), 1)

    def test_every_case(self) -> None:
        self.assertEqual(len(ex.components(ex.adjacency())), 1)
        self.assertEqual(ex.components({"A": []}), [["A"]])
        self.assertEqual(ex.components(ex.adjacency(["A", "B"], [("A", "A")])), [["A"], ["B"]])
        self.assertEqual(ex.strongly_connected({"A": ["B"], "B": ["C"], "C": []}), [["A"], ["B"], ["C"]])
        self.assertEqual(len(ex.strongly_connected({"A": ["B"], "B": ["C"], "C": ["A"]})), 1)
        self.assertEqual(ex.strongly_connected({"A": ["A"]}), [["A"]])
        self.assertEqual(ex.components({}), [])

    def test_finish_lemma(self) -> None:
        t = ex.finish_times(ex.directed())
        self.assertEqual(t["Library"], (1, 16))
        self.assertEqual(t["Harbour"], (8, 9))
        groups = ex.strongly_connected(ex.directed())
        latest = [max(t[v][1] for v in grp) for grp in groups]
        self.assertEqual(latest, [16, 12, 11])
        for i, j in ex.condensation(ex.directed(), groups):       # an arrow between groups i -> j
            self.assertGreater(latest[i], latest[j])
        self.assertEqual(ex.finish_times({}), {})

    def test_tarjan(self) -> None:
        log, final = [], {}
        groups = ex.tarjan_scc(ex.directed(), log, final)
        self.assertEqual(groups, [["Harbour", "Station", "Museum"], ["Hospital"], ["Park", "Market", "School", "Library"]])
        self.assertEqual([(v, d, lo) for v, d, lo, _ in log], [("Museum", 6, 6), ("Hospital", 5, 5), ("Library", 1, 1)])
        self.assertEqual(final["Station"], (7, 6))
        self.assertEqual(final["School"], (2, 1))
        self.assertEqual(ex.tarjan_scc({}), [])
        self.assertEqual(ex.tarjan_scc({"A": []}), [["A"]])
        self.assertEqual(ex.tarjan_scc({"A": ["A"]}), [["A"]])
        self.assertEqual(ex.tarjan_scc({"A": ["B"], "B": ["C"], "C": []}), [["C"], ["B"], ["A"]])
        self.assertEqual(len(ex.tarjan_scc({"A": ["B"], "B": ["C"], "C": ["A"]})), 1)

    def test_tarjan_agrees_with_kosaraju(self) -> None:
        import random
        rng = random.Random(28)
        for _ in range(300):
            n = rng.randint(0, 9)
            g = {v: [w for w in range(n) if rng.random() < 0.25] for v in range(n)}
            a = sorted(sorted(x) for x in ex.tarjan_scc(g))
            b = sorted(sorted(x) for x in ex.strongly_connected(g))
            self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
