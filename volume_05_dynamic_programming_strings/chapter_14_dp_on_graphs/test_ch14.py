import unittest

import ch14_examples as ex


class TestChapter14(unittest.TestCase):
    def test_town(self) -> None:
        dist, ways = ex.count_quickest(ex.adjacency(), "Library")
        self.assertEqual((dist["Harbour"], set(ways.values())), (15, {1}))
        dist, ways = ex.count_quickest(ex.adjacency(ex.PLACES, ex.ROADWORKS), "Library")
        self.assertEqual((dist["Station"], ways["Station"], dist["Harbour"], ways["Harbour"]), (10, 2, 16, 3))
        rows = ex.at_most_k(ex.DEPOTS, ex.LEGS, "A", 4)
        self.assertEqual([r["E"] for r in rows], [float("inf"), float("inf"), 2, 2, -2])
        self.assertEqual(rows[3]["B"], 2)
        course = ["Basics", "Lists", "Trees", "Graphs", "Search", "Project"]
        pre = [("Basics", "Lists"), ("Basics", "Trees"), ("Lists", "Graphs"), ("Trees", "Graphs"), ("Lists", "Search"),
               ("Graphs", "Project"), ("Search", "Project"), ("Trees", "Project")]
        self.assertEqual(ex.count_paths_dag(course, pre, "Basics")["Project"], 4)

    def test_every_case(self) -> None:
        d = ex.adjacency(["A", "B", "C", "D"], [("A", "B", 1), ("A", "C", 1), ("B", "D", 1), ("C", "D", 1)])
        self.assertEqual(ex.count_quickest(d, "A")[1]["D"], 2)
        z = ex.adjacency(["A", "B", "C"], [("A", "B", 0), ("B", "C", 2), ("A", "C", 2)])
        self.assertEqual(ex.count_quickest(z, "A")[1], {"A": 1, "B": 1, "C": 2})
        self.assertIsNone(ex.count_quickest(ex.adjacency(ex.PLACES + ["Island"], ex.ROADS), "Library")[1].get("Island"))
        self.assertEqual((ex.count_quickest({"A": {}}, "A"), ex.at_most_k(["A", "B"], [("A", "B", 3)], "A", 0)),
                         (({"A": 0}, {"A": 1}), [{"A": 0, "B": float("inf")}]))


    def test_slower_school_road(self) -> None:
        roads = [(a, b, 7 if (a, b) == ("School", "Station") else w) for a, b, w in ex.ROADWORKS]
        dist, ways = ex.count_quickest(ex.adjacency(ex.PLACES, roads), "Library")
        self.assertEqual((dist["Station"], ways["Station"], dist["Harbour"], ways["Harbour"]), (10, 1, 16, 2))


if __name__ == "__main__":
    unittest.main()
