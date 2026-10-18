import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestTrees(unittest.TestCase):
    def setUp(self) -> None:
        self.home = ex.sample_folders()

    def test_basic_measures(self) -> None:
        self.assertEqual(ex.count_nodes(self.home), 10)
        self.assertEqual(ex.height(self.home), 3)
        self.assertEqual(ex.leaves(self.home), ["essay.txt", "budget.xlsx", "lion.jpg", "zebra.jpg", "beach.jpg", "notes.txt"])
        self.assertEqual(ex.total_size(self.home), 12 + 30 + 400 + 350 + 500 + 2)
        self.assertEqual(ex.height(ex.TreeNode("solo")), 0)

    def test_show_and_paths(self) -> None:
        lines = list(ex.show(self.home))
        self.assertEqual(lines[0], "home")
        self.assertIn("            lion.jpg", lines)
        self.assertEqual(ex.path_to(self.home, "lion.jpg"), ["home", "photos", "zoo_trip", "lion.jpg"])
        self.assertIsNone(ex.path_to(self.home, "missing"))

    def test_levels(self) -> None:
        self.assertEqual(ex.people_per_level(self.home), [1, 3, 4, 2])
        self.assertEqual(sum(ex.people_per_level(self.home)), ex.count_nodes(self.home))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        home = ex.sample_folders()
        self.assertEqual(sol.largest_folder(home), ("home", 1294))
        self.assertEqual(sol.find_files(home, ".jpg"), ["lion.jpg", "zebra.jpg", "beach.jpg"])
        self.assertEqual(sol.max_children(home), 3)
        t = sol.build_from_paths(["zoo/cats/lion", "zoo/cats/tiger", "zoo/birds/eagle"])
        self.assertEqual(list(ex.show(t)), ["zoo", "    cats", "        lion", "        tiger", "    birds", "        eagle"])


if __name__ == "__main__":
    unittest.main()
