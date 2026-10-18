import unittest

from ch04_examples import (
    baggage_fee,
    banana_advice,
    is_leap_year,
    is_suspicious_payment,
    letter_grade,
    read_age_safely,
    ticket_price,
    triage_level,
)
from ch04_solutions import (
    biggest_of_three,
    can_ride_roller_coaster,
    classify_animal,
    even_or_odd,
    parking_fee,
    shipping_cost,
)


class TestExamples(unittest.TestCase):
    def test_banana(self) -> None:
        self.assertEqual(banana_advice("GREEN"), "Wait a few days")
        self.assertEqual(banana_advice("purple"), "Unknown color - check again")

    def test_ticket_boundaries(self) -> None:
        expected = {0: 0, 2: 0, 3: 80, 12: 80, 13: 150, 59: 150, 60: 100}
        for age, price in expected.items():
            self.assertEqual(ticket_price(age), price, age)
        with self.assertRaises(ValueError):
            ticket_price(-1)

    def test_grades(self) -> None:
        self.assertEqual([letter_grade(s) for s in (100, 90, 89, 75, 60, 40, 39, 0)],
                         ["A", "A", "B", "B", "C", "D", "F", "F"])
        with self.assertRaises(ValueError):
            letter_grade(101)

    def test_leap(self) -> None:
        self.assertTrue(is_leap_year(2024))
        self.assertTrue(is_leap_year(2000))
        self.assertFalse(is_leap_year(1900))
        self.assertFalse(is_leap_year(2023))

    def test_baggage(self) -> None:
        self.assertEqual(baggage_fee(20, False), 0)
        self.assertEqual(baggage_fee(24, False), 40)
        self.assertEqual(baggage_fee(24, True), 0)
        self.assertEqual(baggage_fee(33, True), -1)

    def test_fraud(self) -> None:
        self.assertTrue(is_suspicious_payment(80_000, "India", "Brazil", 1))
        self.assertFalse(is_suspicious_payment(80_000, "India", "India", 1))
        self.assertTrue(is_suspicious_payment(10, "India", "India", 11))

    def test_triage(self) -> None:
        self.assertTrue(triage_level(False, False, 1).startswith("RED"))
        self.assertTrue(triage_level(True, True, 1).startswith("RED"))
        self.assertTrue(triage_level(True, False, 7).startswith("YELLOW"))
        self.assertTrue(triage_level(True, False, 3).startswith("GREEN"))

    def test_read_age(self) -> None:
        self.assertEqual(read_age_safely(" 12 "), 12)
        self.assertIsNone(read_age_safely("twelve"))
        self.assertIsNone(read_age_safely("-5"))


class TestSolutions(unittest.TestCase):
    def test_simple(self) -> None:
        self.assertEqual(even_or_odd(0), "even")
        self.assertEqual(even_or_odd(-3), "odd")
        self.assertEqual(biggest_of_three(4, 9, 2), 9)
        self.assertEqual(biggest_of_three(7, 7, 7), 7)
        self.assertEqual(biggest_of_three(1, 2, 3), 3)

    def test_rules(self) -> None:
        self.assertTrue(can_ride_roller_coaster(130, 10, True))
        self.assertFalse(can_ride_roller_coaster(130, 10, False))
        self.assertFalse(can_ride_roller_coaster(110, 30, True))
        self.assertEqual(parking_fee(1, True), 0)
        self.assertEqual(parking_fee(3, False), 40)
        self.assertEqual(parking_fee(3, True), 80)
        self.assertEqual(parking_fee(20, True), 200)

    def test_tree_and_shipping(self) -> None:
        self.assertEqual(classify_animal(True, True, False), "bird")
        self.assertEqual(classify_animal(False, True, True), "mammal")
        self.assertEqual(classify_animal(False, True, False), "fish")
        self.assertEqual(shipping_cost(300, True), 0)
        self.assertEqual(shipping_cost(600, False), 0)
        self.assertEqual(shipping_cost(500, False), 40)


if __name__ == "__main__":
    unittest.main()
