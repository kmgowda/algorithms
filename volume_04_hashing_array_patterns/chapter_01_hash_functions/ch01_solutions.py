"""Volume 4, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

from ch01_examples import bucket_counts, polynomial_hash


def hash_by_hand(key: str, slots: int, base: int = 31) -> list[int]:
    """Exercise 1: show every step of Horner's rule."""
    steps, h = [], 0
    for ch in key:
        h = (h * base + ord(ch)) % slots
        steps.append(h)
    return steps


def phone_hash(number: str, slots: int) -> int:
    """Exercise 2: use the LAST digits of a phone number - area codes make the first digits repetitive."""
    digits = "".join(ch for ch in number if ch.isdigit())
    return int(digits[-6:] or "0") % slots


def collisions(keys: list[str], slots: int, hash_fn=polynomial_hash) -> int:
    """Exercise 3: number of keys that landed in an already-used slot."""
    return sum(c - 1 for c in bucket_counts(keys, slots, hash_fn) if c > 1)


def tuple_hash(point: tuple[int, int], slots: int) -> int:
    """Exercise 4: hash a grid cell (row, col) by combining both parts, so (1, 2) and (2, 1) differ."""
    r, c = point
    return (r * 1_000_003 + c) % slots


def birthday_probability(people: int, days: int = 365) -> float:
    """Exercise 5: chance that at least two of `people` share a birthday (= at least one hash collision)."""
    p_all_different = 1.0
    for i in range(people):
        p_all_different *= (days - i) / days
    return 1 - p_all_different


if __name__ == "__main__":
    print(hash_by_hand("cat", 101), phone_hash("+91 80 4123 5678", 100))
    print(collisions(["a", "b", "c", "k"], 10), tuple_hash((1, 2), 97) != tuple_hash((2, 1), 97))
    print(round(birthday_probability(23), 3))
