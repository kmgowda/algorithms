import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


def random_graph(rng, n, m):
    g = {v: [] for v in range(n)}
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b and b not in g[a]:
            g[a].append(b)
            g[b].append(a)
    return g


class TestBipartite(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            g = random_graph(rng, rng.randint(1, 7), rng.randint(0, 10))
            chi = sol.chromatic_number(g)
            col = ex.two_color(g)
            self.assertEqual(col is not None, chi <= 2)
            if col is not None:
                self.assertTrue(sol.is_valid_coloring(g, col))
            else:
                cyc = ex.odd_cycle(g)
                self.assertEqual(len(cyc) % 2, 1)
                self.assertEqual(len(set(cyc)), len(cyc))
                self.assertTrue(all(b in g[a] for a, b in zip(cyc, cyc[1:] + cyc[:1])))
            greedy = ex.greedy_coloring(g)
            wp = ex.welsh_powell(g)
            for c in (greedy, wp):
                self.assertTrue(sol.is_valid_coloring(g, c))
                self.assertGreaterEqual(max(c.values()) + 1, chi)
                self.assertLessEqual(max(c.values()) + 1, max(len(v) for v in g.values()) + 1)

    def test_examples(self) -> None:
        teams = {"Ana": ["Ben", "Dev"], "Ben": ["Ana", "Cy"], "Cy": ["Ben", "Dev"], "Dev": ["Cy", "Ana"]}
        self.assertTrue(ex.is_bipartite(teams))
        self.assertIsNone(ex.odd_cycle(teams))
        slots = ex.exam_timetable([("Maths", "Physics"), ("Maths", "Chemistry"), ("Physics", "Biology"),
                                   ("Chemistry", "Biology"), ("Maths", "Biology")])
        self.assertEqual(max(slots.values()) + 1, 3)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertTrue(sol.possible_bipartition(4, [(1, 2), (1, 3), (2, 4)]))
        self.assertFalse(sol.possible_bipartition(3, [(1, 2), (1, 3), (2, 3)]))
        self.assertEqual(sol.bad_greedy_order(), (4, 2))


if __name__ == "__main__":
    unittest.main()
