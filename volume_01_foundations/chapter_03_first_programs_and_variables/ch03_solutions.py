"""Chapter 3 - Solutions to the exercises."""

from __future__ import annotations


def rectangle_garden(length_m: float, width_m: float) -> tuple[float, float]:
    """Exercise 2: area and fence length (perimeter) of a rectangular garden."""
    area = length_m * width_m
    perimeter = 2 * (length_m + width_m)
    return area, perimeter


def minutes_to_hours_and_minutes(total_minutes: int) -> tuple[int, int]:
    """Exercise 3: 135 minutes -> (2, 15)."""
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return hours, minutes


def split_bill(total: float, people: int, tip_percent: float) -> float:
    """Exercise 4: each friend's share of a restaurant bill, including tip."""
    with_tip = total + total * tip_percent / 100
    return round(with_tip / people, 2)


def library_late_fee(days_late: int, fee_per_day: float = 2.5) -> float:
    """Exercise 5: late fee for a library book."""
    return days_late * fee_per_day


def fruit_crates(fruits: int, per_crate: int) -> tuple[int, int]:
    """Exercise 6: full crates and leftover fruits."""
    return fruits // per_crate, fruits % per_crate


def rotate_three(a: str, b: str, c: str) -> tuple[str, str, str]:
    """Exercise 7: three kids rotate seats: a gets b's seat, b gets c's, c gets a's."""
    temporary = a
    a = b
    b = c
    c = temporary
    return a, b, c


if __name__ == "__main__":
    print(rectangle_garden(8, 5))
    print(minutes_to_hours_and_minutes(135))
    print(split_bill(1200, 4, 10))
    print(library_late_fee(6))
    print(fruit_crates(53, 12))
    print(rotate_three("Ana", "Ben", "Cy"))
