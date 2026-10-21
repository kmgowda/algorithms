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


if __name__ == "__main__":
    unittest.main()
