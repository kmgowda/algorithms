import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestBest(unittest.TestCase):
    def test_tallest(self) -> None:
        self.assertEqual(ex.tallest([4.8, 5.6, 5.1, 5.9, 4.3]), 5.9)
        self.assertEqual(ex.tallest([3.0]), 3.0)
        with self.assertRaises(ValueError):
            ex.tallest([])

    def test_against_builtins_on_random_data(self) -> None:
        rng = random.Random(42)
        for _ in range(200):
            values = [rng.randint(-50, 50) for _ in range(rng.randint(2, 30))]
            self.assertEqual(ex.tallest(values), max(values))
            self.assertEqual(sol.smallest(values), min(values))
            self.assertEqual(sol.min_and_max(values), (min(values), max(values)))
            ordered = sorted(values, reverse=True)
            self.assertEqual(ex.two_largest(values), (ordered[0], ordered[1]))
            self.assertEqual(values[ex.index_of_cheapest(values)], min(values))

    def test_cheapest_first_on_tie(self) -> None:
        self.assertEqual(ex.index_of_cheapest([120, 95, 110, 95]), 1)

    def test_top_student(self) -> None:
        self.assertEqual(ex.top_student({"Ana": 88, "Ben": 92, "Cy": 92}), ("Ben", 92))
        with self.assertRaises(ValueError):
            ex.top_student({})


class TestSearch(unittest.TestCase):
    shelf = ["Matilda", "Holes", "Wonder", "Coraline", "Holes"]

    def test_linear_search(self) -> None:
        self.assertEqual(ex.linear_search(self.shelf, "Matilda"), 0)
        self.assertEqual(ex.linear_search(self.shelf, "Holes"), 1)
        self.assertEqual(ex.linear_search(self.shelf, "Dune"), -1)
        self.assertEqual(ex.linear_search([], "Dune"), -1)

    def test_comparisons(self) -> None:
        self.assertEqual(ex.linear_search_counting(self.shelf, "Matilda"), (0, 1))
        self.assertEqual(ex.linear_search_counting(self.shelf, "Dune"), (-1, 5))

    def test_find_all_and_last(self) -> None:
        self.assertEqual(ex.find_all(self.shelf, "Holes"), [1, 4])
        self.assertEqual(sol.last_index_of(self.shelf, "Holes"), 4)
        self.assertEqual(sol.last_index_of(self.shelf, "Dune"), -1)

    def test_patient(self) -> None:
        records = [{"id": "P7", "name": "Ana"}, {"id": "P3", "name": "Ben"}]
        self.assertEqual(ex.find_patient(records, "P3"), {"id": "P3", "name": "Ben"})
        self.assertIsNone(ex.find_patient(records, "P9"))


class TestQuestions(unittest.TestCase):
    def test_any_all(self) -> None:
        self.assertTrue(ex.any_overdrawn([200.0, -3.0]))
        self.assertFalse(ex.any_overdrawn([]))
        self.assertFalse(ex.all_vaccinated({"lion": True, "otter": False}))
        self.assertTrue(ex.all_vaccinated({}))

    def test_seller_and_average(self) -> None:
        self.assertEqual(ex.cheapest_seller([("A", 499, False), ("B", 520, True), ("C", 510, True)]), "C")
        self.assertIsNone(ex.cheapest_seller([("A", 499, False)]))
        self.assertEqual(ex.running_average([20, 22, 27, 19]), [20.0, 21.0, 23.0, 22.0])


class TestSolutions(unittest.TestCase):
    def test_misc(self) -> None:
        self.assertEqual(sol.count_above([31, 28, 35, 30], 30), 2)
        self.assertEqual(sol.longest_word("the hippopotamus ate grass"), "hippopotamus")
        self.assertEqual(sol.longest_word(""), "")
        self.assertTrue(sol.is_sorted([1, 2, 2, 5]))
        self.assertTrue(sol.is_sorted([]))
        self.assertFalse(sol.is_sorted([1, 3, 2]))

    def test_profit(self) -> None:
        self.assertEqual(sol.best_profit([7, 1, 5, 3, 6, 4]), 5)
        self.assertEqual(sol.best_profit([7, 6, 4, 3, 1]), 0)
        self.assertEqual(sol.best_profit([]), 0)
        rng = random.Random(7)
        for _ in range(200):
            prices = [rng.randint(1, 100) for _ in range(rng.randint(0, 15))]
            brute = max([prices[j] - prices[i] for i in range(len(prices))
                         for j in range(i + 1, len(prices))] + [0])
            self.assertEqual(sol.best_profit(prices), brute)


if __name__ == "__main__":
    unittest.main()
