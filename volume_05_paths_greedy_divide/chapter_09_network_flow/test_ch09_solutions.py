import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


def raises(nodes, edges, s, t, road) -> bool:
    """Brute force: does widening this road by a lot raise the maximum flow?"""
    base = ex.max_flow(nodes, edges, s, t)[0]
    wide = [(a, b, c + 100 if (a, b, c) == road else c) for a, b, c in edges]
    return ex.max_flow(nodes, wide, s, t)[0] > base


class TestChapter9Solutions(unittest.TestCase):
    def test_book_network(self) -> None:
        self.assertEqual(sol.upgradable_roads(ex.NODES, ex.PIPES, "Warehouse", "Library"),
                         [("Bridge", "Library", 7), ("Square", "Library", 6)])

    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.upgradable_roads(["s", "t"], [], "s", "t"), [])
        self.assertEqual(sol.upgradable_roads(["s", "t"], [("s", "t", 3)], "s", "t"), [("s", "t", 3)])
        self.assertEqual(sol.upgradable_roads(["s", "t"], [("s", "t", 0)], "s", "t"), [("s", "t", 0)])
        self.assertEqual(sol.upgradable_roads(["s", "m", "t"], [("s", "m", 5), ("m", "t", 3)], "s", "t"),
                         [("m", "t", 3)])
        tie = [("s", "m", 3), ("m", "t", 3)]                     # two minimum cuts: neither road alone helps
        self.assertEqual(sol.upgradable_roads(["s", "m", "t"], tie, "s", "t"), [])
        d = [("s", "a", 1), ("a", "b", 1), ("b", "t", 1), ("s", "b", 1), ("a", "t", 1)]
        self.assertEqual(sol.upgradable_roads(["s", "a", "b", "t"], d, "s", "t"), [])

    def test_against_brute_force(self) -> None:
        rng = random.Random(5)
        for _ in range(150):
            nodes = ["s", "a", "b", "c", "t"]
            pairs = [(x, y) for x in nodes for y in nodes if x != y and x != "t" and y != "s"]
            chosen = rng.sample(pairs, rng.randint(0, 7))
            chosen = [(x, y) for x, y in chosen if (y, x) not in chosen or x < y]
            edges = [(x, y, rng.randint(0, 4)) for x, y in chosen]
            got = sol.upgradable_roads(nodes, edges, "s", "t")
            self.assertEqual(got, [e for e in edges if raises(nodes, edges, "s", "t", e)])

    def test_forward_only_bug(self) -> None:
        side, cap = sol.cut_forward_only(sol.TRAP_NODES, sol.TRAP, "s", "t")
        self.assertEqual((side, cap), ({"s", "b", "c"}, 4))
        self.assertEqual(ex.max_flow(sol.TRAP_NODES, sol.TRAP, "s", "t")[0], 2)
        self.assertEqual(ex.min_cut(sol.TRAP_NODES, sol.TRAP, "s", "t"), ({"s", "a", "b", "c"}, [("c", "t", 2)]))


if __name__ == "__main__":
    unittest.main()
