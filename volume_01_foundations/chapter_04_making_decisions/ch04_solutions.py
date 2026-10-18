"""Chapter 4 - Solutions to the exercises."""

from __future__ import annotations


def even_or_odd(number: int) -> str:
    """Exercise 1."""
    return "even" if number % 2 == 0 else "odd"


def biggest_of_three(a: int, b: int, c: int) -> int:
    """Exercise 2: without using the built-in max()."""
    if a >= b and a >= c:
        return a
    if b >= c:
        return b
    return c


def can_ride_roller_coaster(height_cm: int, age: int, with_adult: bool) -> bool:
    """Exercise 3: at least 120 cm, and either 12+ years old or with an adult."""
    return height_cm >= 120 and (age >= 12 or with_adult)


def parking_fee(hours: int, is_weekend: bool) -> int:
    """Exercise 4: first hour free, then 20 per hour; weekends double; max 200."""
    if hours <= 1:
        return 0
    fee = (hours - 1) * 20
    if is_weekend:
        fee *= 2
    return min(fee, 200)


def classify_animal(has_feathers: bool, lives_in_water: bool, has_fur: bool) -> str:
    """Exercise 5: a tiny decision tree."""
    if has_feathers:
        return "bird"
    if has_fur:
        return "mammal"
    if lives_in_water:
        return "fish"
    return "reptile or other"


def shipping_cost(total: float, is_member: bool) -> int:
    """Exercise 6: members always ship free; others ship free above 500, else 40."""
    if is_member or total > 500:
        return 0
    return 40


if __name__ == "__main__":
    print(even_or_odd(7), biggest_of_three(4, 9, 2), can_ride_roller_coaster(130, 10, True))
    print(parking_fee(5, True), classify_animal(False, True, False), shipping_cost(300, False))
