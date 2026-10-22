import random
import unittest

import ch26_examples as ex
import ch26_solutions as sol


class TestTreeCover(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.tree_cover([]), set())
        self.assertEqual(len(sol.tree_cover([("a", "b")])), 1)
        self.assertEqual(sol.tree_cover([("a", "b"), ("b", "c")]), {"b"})
        self.assertEqual(sol.tree_cover([("c", x) for x in "pqrs"]), {"c"})

    def test_town_tree(self) -> None:
        tree = [("Library", "Park"), ("Library", "School"), ("Park", "Market"), ("Market", "Station"),
                ("Station", "Museum"), ("Museum", "Harbour"), ("Museum", "Hospital")]
        self.assertEqual(len(sol.tree_cover(tree)), 3)

    def test_random_forests_are_optimal(self) -> None:
        r = random.Random(26)
        for _ in range(200):
            n = r.randint(1, 9)
            edges = [(v, r.randrange(v)) for v in range(1, n) if r.random() < 0.85]
            c = sol.tree_cover(edges)
            self.assertTrue(all(a in c or b in c for a, b in edges))
            self.assertEqual(len(c), len(ex.smallest_cover(list(range(n)), edges)))


if __name__ == "__main__":
    unittest.main()
