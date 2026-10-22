import random
import unittest

import ch01_solutions as sol


class TestChapter28Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.compressed_from_edges(0, []), ([0], []))
        self.assertEqual(sol.compressed_from_edges(1, []), ([0, 0], []))
        self.assertEqual(sol.compressed_from_edges(1, [(0, 0)]), ([0, 1], [0]))          # a self-loop
        self.assertEqual(sol.compressed_from_edges(2, [(0, 1), (0, 1)]), ([0, 2, 2], [1, 1]))  # a repeat

    def test_example(self) -> None:
        edges = [(0, 1), (0, 2), (1, 2), (2, 0), (3, 2)]
        self.assertEqual(sol.compressed_from_edges(4, edges), ([0, 2, 3, 4, 5], [1, 2, 2, 0, 2]))
        self.assertEqual(sol.reverse_compressed(4, *sol.compressed_from_edges(4, edges)),
                         ([0, 1, 2, 5, 5], [2, 0, 0, 1, 3]))

    def test_against_lists(self) -> None:
        rng = random.Random(2)
        for n in range(1, 30):
            edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randrange(3 * n))]
            start, targets = sol.compressed_from_edges(n, edges)
            for v in range(n):
                self.assertEqual(targets[start[v]:start[v + 1]], [b for a, b in edges if a == v])
            rs, rt = sol.reverse_compressed(n, start, targets)
            for v in range(n):
                self.assertEqual(sorted(rt[rs[v]:rs[v + 1]]), sorted(a for a, b in edges if b == v))

    def test_matrix_search_cost(self) -> None:
        self.assertEqual((sol.matrix_cells_read(1), sol.matrix_cells_read(2000)), (1, 4_000_000))


if __name__ == "__main__":
    unittest.main()
