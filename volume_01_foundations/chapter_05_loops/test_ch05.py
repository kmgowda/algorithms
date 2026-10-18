import unittest

from ch05_examples import (
    bus_countdown,
    check_pin,
    connect_with_retries,
    count_letter,
    count_sheep,
    plant_growth,
    seating_chart,
    skip_closed_days,
    sum_up_to,
    times_table,
    years_to_reach,
)
from ch05_solutions import (
    count_vowels,
    days_until_full,
    digit_sum,
    even_numbers_up_to,
    factorial,
    fizz_buzz,
    triangle,
)


class TestExamples(unittest.TestCase):
    def test_sheep_and_countdown(self) -> None:
        self.assertEqual(count_sheep(2), "1 sheep... 2 sheep... Zzz")
        self.assertEqual(count_sheep(0), "Zzz")
        self.assertEqual(bus_countdown(2), ["2 stops to go", "1 stops to go", "This is your stop!"])
        self.assertEqual(bus_countdown(0), ["This is your stop!"])

    def test_table_and_sum(self) -> None:
        self.assertEqual(times_table(7, 2), "7 x 1 = 7\n7 x 2 = 14")
        self.assertEqual(sum_up_to(100), 5050)
        self.assertEqual(sum_up_to(0), 0)
        for n in range(50):
            self.assertEqual(sum_up_to(n), n * (n + 1) // 2)

    def test_count_letter(self) -> None:
        self.assertEqual(count_letter("banana", "a"), 3)
        self.assertEqual(count_letter("", "a"), 0)

    def test_years(self) -> None:
        self.assertEqual(years_to_reach(1000, 2000, 7), 11)
        self.assertEqual(years_to_reach(2000, 1000, 7), 0)
        with self.assertRaises(ValueError):
            years_to_reach(1000, 2000, 0)

    def test_retries(self) -> None:
        self.assertEqual(connect_with_retries([False, False, True]), (True, [1, 2]))
        self.assertEqual(connect_with_retries([True]), (True, []))
        self.assertEqual(connect_with_retries([], max_attempts=4), (False, [1, 2, 4, 8]))

    def test_break_continue(self) -> None:
        self.assertEqual(check_pin(["1111", "4321"], "4321"), "Welcome! (try 2)")
        self.assertEqual(check_pin(["1", "2", "3", "4321"], "4321"), "Card blocked")
        self.assertEqual(skip_closed_days(["Monday", "Friday", "Monday"]), ["Friday"])

    def test_nested(self) -> None:
        self.assertEqual(seating_chart(2, 3), ["A1", "A2", "A3", "B1", "B2", "B3"])
        self.assertEqual(seating_chart(0, 3), [])

    def test_plant(self) -> None:
        self.assertEqual(plant_growth(10, 0), 10)
        self.assertEqual(plant_growth(10, 1), 11.0)


class TestSolutions(unittest.TestCase):
    def test_basics(self) -> None:
        self.assertEqual(even_numbers_up_to(10), [2, 4, 6, 8, 10])
        self.assertEqual(even_numbers_up_to(1), [])
        self.assertEqual([factorial(n) for n in range(6)], [1, 1, 2, 6, 24, 120])
        with self.assertRaises(ValueError):
            factorial(-1)
        self.assertEqual(count_vowels("Elephant"), 3)
        self.assertEqual(digit_sum(4096), 19)
        self.assertEqual(digit_sum(0), 0)
        self.assertEqual(digit_sum(-42), 6)

    def test_fizz_buzz(self) -> None:
        result = fizz_buzz(15)
        self.assertEqual(result[2], "Fizz")
        self.assertEqual(result[4], "Buzz")
        self.assertEqual(result[14], "FizzBuzz")
        self.assertEqual(result[0], "1")

    def test_triangle_tank(self) -> None:
        self.assertEqual(triangle(3), "*\n**\n***")
        self.assertEqual(days_until_full(100, 15, 5), 10)
        self.assertEqual(days_until_full(100, 5, 5), -1)


if __name__ == "__main__":
    unittest.main()
