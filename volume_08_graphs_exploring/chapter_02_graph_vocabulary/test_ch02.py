import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestVocabulary(unittest.TestCase):
    def setUp(self) -> None:
        self.friends = {"Ana": ["Ben", "Cy"], "Ben": ["Ana", "Cy"], "Cy": ["Ana", "Ben", "Dev"], "Dev": ["Cy"]}

    def test_paths_and_cycles(self) -> None:
        self.assertTrue(ex.is_undirected(self.friends))
        self.assertTrue(ex.is_cycle(self.friends, ["Ana", "Ben", "Cy", "Ana"]))
        self.assertFalse(ex.is_cycle(self.friends, ["Ana", "Ben", "Ana"]))           # going back on one edge
        self.assertTrue(ex.is_simple_path(self.friends, ["Ana", "Cy", "Dev"]))
        self.assertFalse(ex.is_path(self.friends, ["Ana", "Dev"]))
        self.assertFalse(ex.is_cycle({"a": ["b"], "b": ["a"], "c": []}, ["a", "b", "a"]))
        self.assertTrue(ex.is_cycle({"a": ["b"], "b": ["c"], "c": ["a"]}, ["a", "b", "c", "a"]))

    def test_handshake_random(self) -> None:
        rng = random.Random(1)
        for _ in range(50):
            g = {v: [] for v in range(10)}
            for _ in range(rng.randint(0, 25)):
                a, b = rng.randrange(10), rng.randrange(10)
                if a != b and b not in g[a]:
                    g[a].append(b)
                    g[b].append(a)
            self.assertTrue(ex.handshake_check(g))
            self.assertTrue(ex.is_undirected(g))

    def test_directed(self) -> None:
        follows = {"ana": ["zoo"], "ben": ["zoo", "ana"], "cy": ["zoo"], "zoo": []}
        self.assertFalse(ex.is_undirected(follows))
        self.assertEqual(ex.in_out_degrees(follows)["zoo"], (3, 0))
        self.assertEqual(ex.influencers(follows, 2), ["zoo", "ana"])
        roads = {"Pune": {"Mumbai": 150}, "Mumbai": {"Surat": 280}, "Surat": {}}
        self.assertEqual(ex.path_length(roads, ["Pune", "Mumbai", "Surat"]), 430)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.find_judge(3, [(1, 3), (2, 3)]), 3)
        self.assertEqual(sol.find_judge(3, [(1, 3), (2, 3), (3, 1)]), -1)
        self.assertEqual((sol.max_edges(5, False), sol.max_edges(5, True)), (10, 20))
        self.assertAlmostEqual(sol.density({"a": ["b"], "b": ["a", "c"], "c": ["b"]}), 2 / 3)
        self.assertEqual(sol.sources_and_sinks({"wake": ["dress"], "dress": ["school"], "school": []}), (["wake"], ["school"]))


if __name__ == "__main__":
    unittest.main()
