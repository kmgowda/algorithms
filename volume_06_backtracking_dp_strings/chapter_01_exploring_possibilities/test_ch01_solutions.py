import itertools
import unittest

import ch01_solutions as sol


class TestChapter01Solutions(unittest.TestCase):
    def test_kth_seating(self) -> None:
        readers = ["Dev", "Ana", "Cai", "Ben"]
        every = [list(p) for p in itertools.permutations(sorted(readers))]
        self.assertEqual([sol.kth_seating(readers, k) for k in range(24)], every)
        self.assertEqual(sol.kth_seating(["Ana", "Ben", "Cai", "Dev"], 13), ["Cai", "Ana", "Dev", "Ben"])
        self.assertEqual(sol.kth_seating([], 0), [])
        self.assertEqual(sol.kth_seating(["Ana"], 0), ["Ana"])
        with self.assertRaises(IndexError):
            sol.kth_seating(["Ana", "Ben"], 2)

    def test_floor_e(self) -> None:
        self.assertTrue(all(sol.tree_nodes_floor_e(n) for n in range(1, 13)))


if __name__ == "__main__":
    unittest.main()
