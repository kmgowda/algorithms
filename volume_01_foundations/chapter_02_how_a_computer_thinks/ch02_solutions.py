"""Chapter 2 - Solutions to the exercises."""

from __future__ import annotations


def binary_to_decimal(bits: str) -> int:
    """Exercise 3: turn a string of bits like "1011" into a normal number (11).

    Read the bits from left to right. Each time: double what you have, then add the new bit.
    """
    value = 0
    for bit in bits:
        if bit not in "01":
            raise ValueError("bits must be 0 or 1")
        value = value * 2 + int(bit)
    return value


def seconds_in_a_week() -> int:
    """Exercise 4."""
    return 7 * 24 * 60 * 60


def bytes_for_photos(photos: int, megabytes_each: int) -> int:
    """Exercise 5: how many bytes do the photos need? (1 megabyte = 1,000,000 bytes here)."""
    return photos * megabytes_each * 1_000_000


def where_to_keep(needed_after_power_off: bool, needed_right_now: bool) -> str:
    """Exercise 6: memory (fast, temporary) or storage (slower, permanent)?"""
    if needed_after_power_off:
        return "storage"
    if needed_right_now:
        return "memory"
    return "nowhere - delete it"


if __name__ == "__main__":
    print(binary_to_decimal("1011"))
    print(seconds_in_a_week())
    print(bytes_for_photos(200, 3))
    print(where_to_keep(True, False))
