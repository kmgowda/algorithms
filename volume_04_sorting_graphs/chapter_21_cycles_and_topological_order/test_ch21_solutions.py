import itertools
import random
import unittest

import ch21_examples as ex
import ch21_solutions as sol


def is_cycle(g, loop):
    return len(loop) >= 2 and loop[0] == loop[-1] and all(b in g[a] for a, b in zip(loop, loop[1:]))


class TestChapter21Solutions(unittest.TestCase):
    def test_atlas(self) -> None:
        self.assertEqual(sol.order_or_cycle(ex.graph()), ("order", ex.TASKS))
        kind, loop = sol.order_or_cycle(ex.graph(needs=ex.NEEDS + [("Label", "Clean pages")]))
        self.assertEqual(kind, "cycle")
        self.assertEqual(loop, ["Dry pages", "Resew spine", "Glue spine", "New cover", "Label", "Clean pages",
                                "Dry pages"])

    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.order_or_cycle({}), ("order", []))
        self.assertEqual(sol.order_or_cycle({"A": []}), ("order", ["A"]))
        self.assertEqual(sol.order_or_cycle({"A": ["A"]}), ("cycle", ["A", "A"]))
        self.assertEqual(sol.order_or_cycle({"A": ["B"], "B": ["A"]}), ("cycle", ["B", "A", "B"]))
        kind, loop = sol.order_or_cycle({"D": ["A"], "A": ["B"], "B": ["C"], "C": ["A"]})
        self.assertEqual((kind, sorted(loop[:-1])), ("cycle", ["A", "B", "C"]))

    def test_random_graphs(self) -> None:
        rng = random.Random(21)
        for _ in range(400):
            n = rng.randint(0, 8)
            g = {v: [w for w in range(n) if rng.random() < 0.2] for v in range(n)}
            kind, out = sol.order_or_cycle(g)
            if kind == "order":
                self.assertTrue(ex.is_valid_order(g, out))
            else:
                self.assertTrue(is_cycle(g, out), (g, out))
                self.assertIsNone(ex.kahn(g))

    def test_unique_order_iff_path(self) -> None:
        """Thinking Problem 1: exactly one order exactly when consecutive tasks of an order are joined by arrows."""
        rng = random.Random(1)
        for _ in range(300):
            n = rng.randint(0, 6)
            g = {v: [w for w in range(v + 1, n) if rng.random() < 0.5] for v in range(n)}
            count = sum(ex.is_valid_order(g, list(p)) for p in itertools.permutations(range(n)))
            order = ex.kahn(g)
            path = all(b in g[a] for a, b in zip(order, order[1:]))
            self.assertEqual(count == 1, path)

    def test_discovery_order_is_wrong(self) -> None:
        g = ex.graph()
        order = sol.discovery_order(g)
        self.assertEqual(order[-1], "Dry pages")
        self.assertFalse(ex.is_valid_order(g, order))
        self.assertEqual(sol.discovery_order({"A": ["B"], "B": [], "C": ["A"]}), ["A", "B", "C"])
        self.assertEqual(sol.discovery_order({}), [])


if __name__ == "__main__":
    unittest.main()
