import unittest

import ch06_examples as ex
from ch06_solutions import (
    bmi,
    bus_trip_cost,
    count_multiples,
    describe_bmi,
    is_adult,
    is_prime,
    kilometers_to_miles,
    late_fee,
    square,
)


class TestExamples(unittest.TestCase):
    def test_reuse(self) -> None:
        self.assertEqual(ex.make_tea(2)[0], "boil 2 cup(s) of water")
        self.assertEqual(ex.boil_egg(3)[0], "boil 2 cup(s) of water")

    def test_defaults(self) -> None:
        self.assertEqual(ex.greet("Maya"), "Hello, Maya!")
        self.assertEqual(ex.greet("Leo", greeting="Hi"), "Hi, Leo!")

    def test_paint(self) -> None:
        self.assertEqual(ex.paint_cans_needed(12, 3), 4)   # 36 m2 -> 3.6 cans -> 4
        self.assertEqual(ex.paint_cans_needed(10, 3), 3)   # exactly 3 cans
        self.assertAlmostEqual(ex.circle_area(1), 3.14159, places=4)

    def test_report(self) -> None:
        self.assertEqual(ex.report_card_line("Aisha", 78, 85, 69), "Aisha: average 77.3, PASS")
        self.assertEqual(ex.report_card_line("Tom", 30, 20, 40), "Tom: average 30.0, FAIL")
        with self.assertRaises(ValueError):
            ex.average(10, 0)

    def test_transfer(self) -> None:
        self.assertEqual(ex.transfer(1000, 200, 300), (700, 500, "Success"))
        self.assertEqual(ex.transfer(100, 200, 300)[2], "Rejected: insufficient funds")
        self.assertEqual(ex.transfer(100, 200, -5)[2], "Rejected: amount must be positive")

    def test_checkout(self) -> None:
        self.assertEqual(ex.checkout_price(450, "SAVE10"), 445.0)
        self.assertEqual(ex.checkout_price(1000, "HALF"), 540.0)
        self.assertEqual(ex.checkout_price(600), 600.0)
        self.assertEqual(ex.checkout_price(600, "BOGUS"), 600.0)

    def test_scope_and_side_effects(self) -> None:
        self.assertEqual(ex.describe_scope(), "City Zoo had 120 visitors")
        self.assertEqual(ex.add_points_pure(10, 5), 15)
        before = len(ex.game_log)
        ex.add_points_with_log(10, 5)
        self.assertEqual(len(ex.game_log), before + 1)


class TestSolutions(unittest.TestCase):
    def test_small(self) -> None:
        self.assertEqual(square(-3), 9)
        self.assertFalse(is_adult(17))
        self.assertTrue(is_adult(17, adult_age=16))
        self.assertAlmostEqual(kilometers_to_miles(10), 6.21371)

    def test_bmi(self) -> None:
        self.assertEqual(bmi(70, 1.75), 22.9)
        self.assertEqual(describe_bmi(70, 1.75), "BMI 22.9 (healthy)")
        with self.assertRaises(ValueError):
            bmi(70, 0)

    def test_counts(self) -> None:
        self.assertEqual(count_multiples(100, 7), 14)
        self.assertEqual(bus_trip_cost(3), 15)
        self.assertEqual(bus_trip_cost(12), 40)

    def test_late_fee(self) -> None:
        self.assertEqual(late_fee(5, False), 10.0)
        self.assertEqual(late_fee(5, True), 5.0)
        self.assertEqual(late_fee(0, False), 0.0)
        self.assertEqual(late_fee(-3, False), 0.0)

    def test_prime(self) -> None:
        self.assertEqual([n for n in range(30) if is_prime(n)], [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])


if __name__ == "__main__":
    unittest.main()
