"""Volume 1, Chapter 2 - How a Computer Carries Out an Algorithm.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


def to_binary(n: int) -> str:
    """Write a whole number n >= 0 in binary, by repeatedly dividing by 2 (Section 2.5)."""
    if n == 0:
        return "0"
    digits = ""
    while n > 0:
        digits = str(n % 2) + digits
        n = n // 2
    return digits


def from_binary(bits: str) -> int:
    """Read a binary number: each position is worth twice the one to its right (Figure 2.3)."""
    value = 0
    for bit in bits:
        value = value * 2 + int(bit)
    return value


def trace_sum(shelf: list[int], count: int, start: int = 0) -> list[int]:
    """The value of `total` after each step of Section 2.7's program (Figure 2.5)."""
    total = start
    snapshots = [total]
    for k in range(count):
        total = total + shelf[k]
        snapshots.append(total)
    return snapshots


def swap_by_arithmetic(a: int, b: int) -> list[tuple[int, int]]:
    """Practice Problem 2: (a, b) after each of a <- a + b, b <- a - b, a <- a - b, starting from (a, b)."""
    states = [(a, b)]
    a = a + b
    states.append((a, b))
    b = a - b
    states.append((a, b))
    a = a - b
    states.append((a, b))
    return states


if __name__ == "__main__":
    print(to_binary(77), from_binary("01001101"), from_binary("00101010"), to_binary(13))
    print(trace_sum(SHELF, 3), trace_sum(SHELF, 3, start=7)[-1])
