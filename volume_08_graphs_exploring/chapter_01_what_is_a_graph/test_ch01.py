import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestGraphBasics(unittest.TestCase):
    def setUp(self) -> None:
        self.roads = ex.make_undirected([("Pune", "Mumbai"), ("Mumbai", "Surat"), ("Pune", "Nashik"), ("Goa", "Panaji")])

    def test_reach(self) -> None:
        self.assertTrue(ex.can_reach(self.roads, "Pune", "Surat"))
        self.assertFalse(ex.can_reach(self.roads, "Pune", "Goa"))
        self.assertTrue(ex.can_reach(self.roads, "Goa", "Goa"))

    def test_reach_matches_union_find(self) -> None:
        rng = random.Random(1)
        for _ in range(50):
            n = 12
            edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 14))]
            g = ex.make_undirected(edges)
            for v in range(n):
                g.setdefault(v, [])
            parent = list(range(n))

            def find(x):
                while parent[x] != x:
                    x = parent[x]
                return x
            for a, b in edges:
                parent[find(a)] = find(b)
            for a in range(n):
                for b in range(n):
                    self.assertEqual(ex.can_reach(g, a, b), find(a) == find(b))

    def test_industry(self) -> None:
        friends = ex.make_undirected([("Ana", "Ben"), ("Ana", "Cy"), ("Ben", "Dev"), ("Cy", "Dev"), ("Cy", "Eve")])
        self.assertEqual(ex.friend_suggestions(friends, "Ana"), [("Dev", 2), ("Eve", 1)])
        web = {"home": ["about", "shop"], "about": ["home"], "shop": ["home", "cart"], "cart": ["shop"], "blog": ["home"]}
        self.assertEqual(ex.most_linked_pages(web)[0], ("home", 3))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        g = ex.make_undirected([("Pune", "Mumbai"), ("Mumbai", "Surat"), ("Pune", "Nashik"), ("Goa", "Panaji")])
        self.assertEqual(sol.count_roads(g), 4)
        self.assertIn(sol.most_connected(g), {"Pune", "Mumbai"})
        self.assertEqual(sol.mutual_friends(ex.make_undirected([("a", "c"), ("b", "c")]), "a", "b"), {"c"})
        self.assertEqual(sol.unreachable_from(g, "Pune"), ["Goa", "Panaji"])


if __name__ == "__main__":
    unittest.main()
