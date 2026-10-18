import bisect
import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestBinarySearch(unittest.TestCase):
    def test_words(self) -> None:
        animals = ["ant", "bear", "cat", "deer", "eagle", "fox", "goat", "horse"]
        for index, animal in enumerate(animals):
            self.assertEqual(ex.binary_search(animals, animal), index)
        self.assertEqual(ex.binary_search(animals, "zebra"), -1)
        self.assertEqual(ex.binary_search(animals, "aardvark"), -1)
        self.assertEqual(ex.binary_search([], "cat"), -1)

    def test_against_linear_search_random(self) -> None:
        rng = random.Random(11)
        for _ in range(300):
            items = sorted(set(rng.randint(0, 100) for _ in range(rng.randint(0, 40))))
            target = rng.randint(-5, 105)
            expected = items.index(target) if target in items else -1
            self.assertEqual(ex.binary_search(items, target), expected)
            self.assertEqual(sol.binary_search_recursive(items, target), expected)

    def test_trace(self) -> None:
        self.assertEqual(ex.binary_search_trace([10, 20, 30, 40, 50, 60, 70, 80, 90], 70),
                         [(0, 4, 8), (5, 6, 8)])

    def test_comparisons(self) -> None:
        self.assertEqual(ex.comparisons_linear_vs_binary(100), (100, 7))
        self.assertEqual(ex.comparisons_linear_vs_binary(1_000_000), (1_000_000, 20))


class TestVariants(unittest.TestCase):
    def test_lower_bound_matches_bisect(self) -> None:
        rng = random.Random(5)
        for _ in range(300):
            items = sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 30)))
            wanted = rng.randint(-3, 53)
            self.assertEqual(ex.first_at_or_after(items, wanted), bisect.bisect_left(items, wanted))
            self.assertEqual(sol.search_insert_position(items, wanted), bisect.bisect_left(items, wanted))
            expected_first = bisect.bisect_left(items, wanted) if wanted in items else -1
            self.assertEqual(sol.first_occurrence(items, wanted), expected_first)

    def test_next_bus(self) -> None:
        timetable = [600, 630, 715, 800, 845, 930]
        self.assertEqual(ex.next_bus(timetable, 720), 800)
        self.assertEqual(ex.next_bus(timetable, 715), 715)
        self.assertEqual(ex.next_bus(timetable, 500), 600)
        self.assertIsNone(ex.next_bus(timetable, 1000))

    def test_price_range(self) -> None:
        prices = [99, 149, 199, 249, 299, 349, 499, 999]
        self.assertEqual(ex.count_in_price_range(prices, 150, 350), 4)
        self.assertEqual(ex.count_in_price_range(prices, 149, 149), 1)
        self.assertEqual(ex.count_in_price_range(prices, 1000, 2000), 0)

    def test_first_bad_version(self) -> None:
        for first_bad in range(1, 60):
            calls = []

            def is_bad(version: int, fb: int = first_bad) -> bool:
                calls.append(version)
                return version >= fb

            self.assertEqual(ex.first_bad_version(59, is_bad), first_bad)
            self.assertLessEqual(len(calls), 6)

    def test_square_root(self) -> None:
        for n in range(0, 2000):
            r = ex.integer_square_root(n)
            self.assertTrue(r * r <= n < (r + 1) * (r + 1))
        with self.assertRaises(ValueError):
            ex.integer_square_root(-1)

    def test_find_account(self) -> None:
        accounts = [(1001, "Ana"), (1042, "Ben"), (1300, "Cy")]
        self.assertEqual(ex.find_account(accounts, 1042), "Ben")
        self.assertIsNone(ex.find_account(accounts, 1100))
        self.assertIsNone(ex.find_account(accounts, 9999))


class TestSolutions(unittest.TestCase):
    def test_max_guesses(self) -> None:
        self.assertEqual(sol.max_guesses(100), 7)
        self.assertEqual(sol.max_guesses(1_000_000), 20)
        self.assertEqual(sol.max_guesses(1_000_000_000), 30)

    def test_capacity(self) -> None:
        self.assertEqual(sol.min_daily_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15)
        self.assertEqual(sol.min_daily_capacity([3, 2, 2, 4, 1, 4], 3), 6)
        self.assertEqual(sol.min_daily_capacity([1, 2, 3, 1, 1], 4), 3)


if __name__ == "__main__":
    unittest.main()
