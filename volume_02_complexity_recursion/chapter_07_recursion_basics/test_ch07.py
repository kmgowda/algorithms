import math
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


class TestBasics(unittest.TestCase):
    def test_dolls_and_countdown(self) -> None:
        self.assertEqual(ex.open_dolls(2), ["open doll 2", "open doll 1", "empty - done"])
        self.assertEqual(ex.open_dolls(0), ["empty - done"])
        self.assertEqual(ex.countdown(3), [3, 2, 1, 0])
        for n in range(10):
            self.assertEqual(ex.countdown(n), ex.countdown_loop(n))

    def test_factorial(self) -> None:
        for n in range(15):
            self.assertEqual(ex.factorial(n), math.factorial(n))
        with self.assertRaises(ValueError):
            ex.factorial(-1)

    def test_list_recursions(self) -> None:
        rng = random.Random(1)
        for _ in range(100):
            values = [rng.randint(-50, 50) for _ in range(rng.randint(1, 20))]
            self.assertEqual(ex.sum_list(values), sum(values))
            self.assertEqual(ex.largest(values), max(values))
        self.assertEqual(ex.sum_list([]), 0)
        with self.assertRaises(ValueError):
            ex.largest([])

    def test_text(self) -> None:
        for word in ("", "a", "zoo", "giraffe"):
            self.assertEqual(ex.reverse_text(word), word[::-1])
        self.assertTrue(ex.is_palindrome("racecar"))
        self.assertTrue(ex.is_palindrome("noon"))
        self.assertTrue(ex.is_palindrome(""))
        self.assertFalse(ex.is_palindrome("zebra"))

    def test_nested(self) -> None:
        self.assertEqual(ex.folder_size(ex.SAMPLE_DISK), 4 + 3000 + 2800 + 120 + 450)
        self.assertEqual(ex.folder_size({}), 0)
        self.assertEqual(ex.headcount(ex.SAMPLE_ORG), 7)
        self.assertEqual(ex.headcount({"name": "Solo"}), 1)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.count_up(5), [1, 2, 3, 4, 5])
        self.assertEqual(sol.count_up(0), [])
        self.assertEqual(sol.digit_sum(4096), 19)
        self.assertEqual(sol.digit_sum(7), 7)
        self.assertEqual(sol.count_occurrences(["cat", "dog", "cat"], "cat"), 2)
        self.assertEqual(sol.power(2, 10), 1024)
        self.assertEqual(sol.power(5, 0), 1)
        self.assertEqual(sol.deepest_level(ex.SAMPLE_DISK), 3)
        self.assertEqual(sol.deepest_level({}), 1)
        self.assertEqual(sol.find_person(ex.SAMPLE_ORG, "Nurse B"), ["Director", "Head of Wards", "Nurse B"])
        self.assertIsNone(sol.find_person(ex.SAMPLE_ORG, "Pilot"))


if __name__ == "__main__":
    unittest.main()
