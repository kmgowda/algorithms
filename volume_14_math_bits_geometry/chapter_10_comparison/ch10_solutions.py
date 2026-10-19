"""Volume 14, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

from ch10_examples import choose_approach


def josephus_every_second(n: int) -> int:
    """Exercise 1: for k = 2 there is a true closed form - write n = 2^m + L, the survivor is 2L + 1. O(1)."""
    high = 1 << (n.bit_length() - 1)
    return 2 * (n - high) + 1


def sum_of_squares(n: int) -> int:
    """Exercise 2: 1^2 + 2^2 + ... + n^2 = n(n + 1)(2n + 1) / 6."""
    return n * (n + 1) * (2 * n + 1) // 6


def pick_approaches() -> dict[str, str]:
    """Exercise 3: choose an approach for each question."""
    return {
        "total of 1..n": choose_approach({"closed form known and proven"}),
        "n-th Fibonacci number mod p for n = 10^18": choose_approach({"recurrence with small state"}),
        "average queue length in a busy bank with lunch breaks": choose_approach({"too complex to analyse"}),
        "a brand-new puzzle": choose_approach(set()),
    }


if __name__ == "__main__":
    print(josephus_every_second(41), sum_of_squares(10), pick_approaches())
