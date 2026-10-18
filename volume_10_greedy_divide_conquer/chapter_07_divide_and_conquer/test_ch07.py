import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


class TestDivideAndConquer(unittest.TestCase):
    def test_sorting(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            v = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
            self.assertEqual(ex.merge_sort(v), sorted(v))
            self.assertEqual(sol.three_way_merge_sort(v), sorted(v))
            self.assertEqual(sol.is_sorted_dc(v), v == sorted(v))
            if v:
                self.assertEqual(ex.total_votes(v), sum(v))
            self.assertEqual(sol.count_occurrences(v, 3), v.count(3))

    def test_master_theorem(self) -> None:
        self.assertEqual(ex.master_theorem(2, 2, 1), "Theta(n log n)")
        self.assertEqual(ex.master_theorem(1, 2, 0), "Theta(log n)")
        self.assertEqual(ex.master_theorem(4, 2, 1), "Theta(n^2)")
        self.assertEqual(ex.master_theorem(2, 2, 2), "Theta(n^2)")
        self.assertEqual(ex.master_theorem(7, 2, 2), "Theta(n^2.81)")
        self.assertEqual(ex.recursion_tree_work(16, 2, 2, lambda m: m), [16, 16, 16, 16, 16])
        self.assertEqual(ex.count_calls(8, 2, 2), 15)

    def test_examples(self) -> None:
        total, parts = ex.parallel_sum(list(range(1, 101)), 4)
        self.assertEqual(total, 5050)
        self.assertEqual(len(parts), 4)
        self.assertEqual(sol.tree_height_dc({"left": {"left": None, "right": None}, "right": None}), 2)


if __name__ == "__main__":
    unittest.main()
