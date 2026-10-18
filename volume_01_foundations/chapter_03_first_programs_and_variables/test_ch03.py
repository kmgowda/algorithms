import unittest
from unittest.mock import patch

from ch03_examples import (
    animal_profile,
    bus_fare,
    cart_total,
    celsius_to_fahrenheit,
    greet_from_input,
    savings_after_one_year,
    swap_seats,
)
from ch03_solutions import (
    fruit_crates,
    library_late_fee,
    minutes_to_hours_and_minutes,
    rectangle_garden,
    rotate_three,
    split_bill,
)


class TestExamples(unittest.TestCase):
    def test_animal_profile(self) -> None:
        self.assertEqual(animal_profile(), "Giraffe: 4 legs, 5.5 m tall, mammal: True")

    def test_bus_fare(self) -> None:
        self.assertEqual(bus_fare(2, 3), 105)
        self.assertEqual(bus_fare(0, 0), 0)

    def test_temperature(self) -> None:
        self.assertEqual(celsius_to_fahrenheit(0), 32)
        self.assertEqual(celsius_to_fahrenheit(100), 212)
        self.assertEqual(celsius_to_fahrenheit(-40), -40)

    def test_bank_and_cart(self) -> None:
        self.assertEqual(savings_after_one_year(1000, 5), 1050.0)
        self.assertEqual(cart_total(499.0, 2, 10, 18), 1059.88)

    def test_swap(self) -> None:
        self.assertEqual(swap_seats("Ana", "Ben"), ("Ben", "Ana"))

    def test_greet_from_input(self) -> None:
        with patch("builtins.input", side_effect=["Maya", "12"]):
            self.assertEqual(greet_from_input(), "Hello Maya! Next year you will be 13.")


class TestSolutions(unittest.TestCase):
    def test_garden(self) -> None:
        self.assertEqual(rectangle_garden(8, 5), (40, 26))

    def test_minutes(self) -> None:
        self.assertEqual(minutes_to_hours_and_minutes(135), (2, 15))
        self.assertEqual(minutes_to_hours_and_minutes(59), (0, 59))

    def test_bill_fee_crates(self) -> None:
        self.assertEqual(split_bill(1200, 4, 10), 330.0)
        self.assertEqual(library_late_fee(6), 15.0)
        self.assertEqual(fruit_crates(53, 12), (4, 5))

    def test_rotate(self) -> None:
        self.assertEqual(rotate_three("Ana", "Ben", "Cy"), ("Ben", "Cy", "Ana"))


if __name__ == "__main__":
    unittest.main()
