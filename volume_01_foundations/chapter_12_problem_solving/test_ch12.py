import random
import unittest

import ch12_examples as ex
import ch12_solutions as sol


class TestWorkedProblems(unittest.TestCase):
    def test_missing_ticket_all_versions(self) -> None:
        for tickets, missing in (([3, 0, 1, 5, 4], 2), ([1], 0), ([0], 1), ([0, 1, 2], 3)):
            self.assertEqual(ex.missing_ticket_brute(tickets), missing)
            self.assertEqual(ex.missing_ticket_set(tickets), missing)
            self.assertEqual(ex.missing_ticket_math(tickets), missing)

    def test_first_unique(self) -> None:
        favorites = ["lion", "otter", "lion", "panda", "otter", "zebra"]
        self.assertEqual(ex.first_unique_counting(favorites), "panda")
        self.assertEqual(ex.first_unique_brute(favorites), "panda")
        self.assertIsNone(ex.first_unique_counting(["a", "a"]))
        self.assertIsNone(ex.first_unique_counting([]))

    def test_merge(self) -> None:
        rng = random.Random(3)
        for _ in range(300):
            a = sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 10)))
            b = sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 10)))
            self.assertEqual(ex.merge_two_pointers(a, b), ex.merge_brute(a, b))

    def test_gates(self) -> None:
        self.assertTrue(ex.gate_conflict_sorted([(900, 945), (1000, 1030), (940, 1000)]))
        self.assertFalse(ex.gate_conflict_sorted([(900, 945), (945, 1000)]))
        self.assertFalse(ex.gate_conflict_sorted([]))
        self.assertIsNone(ex.stress_test(ex.gate_conflict_brute, ex.gate_conflict_sorted, ex.random_slots))

    def test_bank_and_hospital(self) -> None:
        self.assertEqual(ex.first_negative_day(100, [-30, 20, -80, -40, 50]), 4)
        self.assertEqual(ex.first_negative_day(100, [10, -20]), -1)
        self.assertEqual(ex.first_negative_day(0, [-1]), 1)
        slots = [900, 930, 1000, 1045, 1130]
        self.assertEqual(ex.earliest_slot(slots, 1020), 1045)
        self.assertEqual(ex.earliest_slot(slots, 900), 900)
        self.assertIsNone(ex.earliest_slot(slots, 1200))

    def test_stress_tester_finds_bugs(self) -> None:
        def buggy(tickets: list[int]) -> int:
            return max(tickets)          # wrong on purpose
        self.assertIsNone(ex.stress_test(ex.missing_ticket_brute, ex.missing_ticket_math, ex.random_tickets))
        self.assertIsNotNone(ex.stress_test(ex.missing_ticket_brute, buggy, ex.random_tickets))


class TestSolutions(unittest.TestCase):
    def test_duplicate(self) -> None:
        self.assertTrue(sol.contains_duplicate([4, 1, 7, 1]))
        self.assertFalse(sol.contains_duplicate([]))
        self.assertFalse(sol.contains_duplicate([1, 2, 3]))

    def test_palindrome(self) -> None:
        self.assertTrue(sol.is_clean_palindrome("A man, a plan, a canal: Panama"))
        self.assertFalse(sol.is_clean_palindrome("race a car"))
        self.assertTrue(sol.is_clean_palindrome(" "))
        self.assertTrue(sol.is_clean_palindrome(".,"))

    def test_move_zeros(self) -> None:
        rng = random.Random(9)
        for _ in range(200):
            values = [rng.choice([0, 0, 1, 2, 3]) for _ in range(rng.randint(0, 12))]
            expected = [v for v in values if v != 0] + [0] * values.count(0)
            sol.move_zeros_to_end(values)
            self.assertEqual(values, expected)

    def test_squares(self) -> None:
        rng = random.Random(4)
        for _ in range(200):
            values = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 12)))
            self.assertEqual(sol.squares_sorted(values), sorted(v * v for v in values))

    def test_majority_and_streak(self) -> None:
        self.assertEqual(sol.majority_vote(["cat", "dog", "cat", "cat"]), "cat")
        self.assertIsNone(sol.majority_vote(["cat", "dog"]))
        self.assertIsNone(sol.majority_vote([]))
        self.assertEqual(sol.longest_streak([10, 4, 20, 1, 3, 2, 11]), 4)
        self.assertEqual(sol.longest_streak([]), 0)
        self.assertEqual(sol.longest_streak([5, 5, 5]), 1)


if __name__ == "__main__":
    unittest.main()
