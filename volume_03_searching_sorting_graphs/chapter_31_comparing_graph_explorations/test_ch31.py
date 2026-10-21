import unittest

import ch31_examples as ex


class TestChapter31(unittest.TestCase):
    def test_town(self) -> None:
        a = ex.town_answers()
        self.assertEqual(list(a.values()), [3, 5, 1, False, 0, 0])

    def test_every_case(self) -> None:
        A, W = ex.bfs_m.adjacency, ex.weak_m
        graphs = {"town": (ex.PLACES, ex.ROADS, (8, 5, 1, False, 0, 0)),
                  "district": (ex.PLACES + W.OUTER, ex.ROADS + W.OUTER_ROADS, (10, 5, 1, False, 2, 2)),
                  "tree": ("ABCD", [("A", "B"), ("B", "C"), ("B", "D")], (4, 0, 1, True, 3, 1)),
                  "square": ("ABCD", [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")], (4, 1, 1, True, 0, 0)),
                  "triangle": ("ABC", [("A", "B"), ("B", "C"), ("C", "A")], (3, 1, 1, False, 0, 0)),
                  "pairs": ("ABCD", [("A", "B"), ("C", "D")], (2, 0, 2, True, 2, 0)),
                  "one": ("A", [], (1, 0, 1, True, 0, 0))}
        for name, (places, roads, want) in graphs.items():
            adj = A(list(places), roads)
            d = ex.dfs_m.dfs(adj, list(places)[0])
            w = ex.weak_m.weak_links(adj)
            got = (len(d["order"]), sum(1 for e in d["edges"] if e[2] == "back"), len(ex.comp_m.components(adj)),
                   ex.bip_m.two_colour(adj)[0] is not None, len(w["bridges"]), len(w["cuts"]))
            self.assertEqual(got, want, name)

    def test_timings_run(self) -> None:
        t = ex.timings(300, 900)
        self.assertEqual(len(t), 7)


if __name__ == "__main__":
    unittest.main()
