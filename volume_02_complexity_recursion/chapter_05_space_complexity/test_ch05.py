import random
import sys
import unittest

import ch05_examples as ex
import ch05_solutions as sol


class TestSpace(unittest.TestCase):
    def test_unique(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            ids = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 15)))
            expected = sorted(set(ids))
            self.assertEqual(ex.unique_sorted_with_set(ids), expected)
            count = ex.unique_sorted_in_place(ids)
            self.assertEqual(ids[:count], expected)

    def test_memory_grows_with_list_but_not_generator(self) -> None:
        self.assertLess(ex.list_memory_bytes(10), ex.list_memory_bytes(1000))
        small = sys.getsizeof(ex.squares_generator(10))
        big = sys.getsizeof(ex.squares_generator(10_000_000))
        self.assertEqual(small, big)
        self.assertEqual(ex.bytes_needed(10, 8), 80)

    def test_generator_values(self) -> None:
        self.assertEqual(list(ex.squares_generator(5)), ex.squares_list(5))
        self.assertEqual(sum(ex.squares_generator(1000)), sum(ex.squares_list(1000)))

    def test_logs(self) -> None:
        self.assertEqual(ex.count_errors(ex.fake_log(100_000)), 2000)
        self.assertEqual(ex.count_errors(["x ERROR y", "x INFO y"]), 1)

    def test_prefix(self) -> None:
        visitors = [120, 340, 90, 410, 500, 220, 610]
        totals = ex.prefix_totals(visitors)
        for a in range(len(visitors)):
            for b in range(a, len(visitors)):
                self.assertEqual(ex.visitors_between(totals, a, b), ex.visitors_between_slow(visitors, a, b))

    def test_bits(self) -> None:
        for number in list(range(0, 5000)) + [2 ** 64 - 1, 2 ** 100]:
            self.assertEqual(ex.count_set_bits(number), bin(number).count("1"))
        with self.assertRaises(ValueError):
            ex.count_set_bits(-1)


class TestSolutions(unittest.TestCase):
    def test_running_max(self) -> None:
        self.assertEqual(list(sol.running_max([21, 19, 25, 24, 30])), [21, 21, 25, 25, 30])
        self.assertEqual(list(sol.running_max([])), [])

    def test_evens_first(self) -> None:
        rng = random.Random(8)
        for _ in range(200):
            values = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
            original = sorted(values)
            sol.move_evens_first(values)
            self.assertEqual(sorted(values), original)
            evens = sum(1 for v in values if v % 2 == 0)
            self.assertTrue(all(v % 2 == 0 for v in values[:evens]))

    def test_ranges_memory_stream(self) -> None:
        self.assertEqual(sol.answer_range_questions([5, 1, 4, 2], [(0, 1), (1, 3), (2, 2)]), [6, 7, 4])
        self.assertTrue(sol.fits_in_memory(100_000_000, 8, 4))
        self.assertFalse(sol.fits_in_memory(1_000_000_000, 8, 4))
        self.assertEqual(sol.average_of_stream(x for x in range(1, 101)), 50.5)
        with self.assertRaises(ValueError):
            sol.average_of_stream([])


if __name__ == "__main__":
    unittest.main()
