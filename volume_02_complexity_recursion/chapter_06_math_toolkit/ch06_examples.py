"""Volume 2, Chapter 6 - The Math Toolkit: Sums, Powers, and Logarithms.

Every formula is paired with a loop that computes the same thing the slow way,
so you can check the math with your own eyes.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import math


# ------------------------------------------------------------------ arithmetic sums
def sum_loop(first: int, last: int, step: int = 1) -> int:
    total = 0
    for value in range(first, last + 1, step):
        total += value
    return total


def arithmetic_sum(first: int, last: int, count: int) -> int:
    """Sum of an evenly spaced sequence = count x (first + last) / 2."""
    return count * (first + last) // 2


def sum_of_squares(n: int) -> int:
    """1^2 + 2^2 + ... + n^2 = n(n+1)(2n+1)/6."""
    return n * (n + 1) * (2 * n + 1) // 6


# ------------------------------------------------------------------ geometric sums
def geometric_sum_loop(first: float, ratio: float, terms: int) -> float:
    total, term = 0.0, first
    for _ in range(terms):
        total += term
        term *= ratio
    return total


def geometric_sum(first: float, ratio: float, terms: int) -> float:
    """first + first*r + ... + first*r^(terms-1) = first * (r^terms - 1) / (r - 1), for r != 1."""
    if ratio == 1:
        return first * terms
    return first * (ratio ** terms - 1) / (ratio - 1)


def chessboard_grains() -> int:
    """1 grain on the first square, doubling each square, 64 squares: 2^64 - 1."""
    return 2 ** 64 - 1


def total_backoff_wait(retries: int, first_wait: float = 1.0) -> float:
    """Industry example: retries wait 1, 2, 4, ... seconds (V1-C5). Total = a geometric sum."""
    return geometric_sum(first_wait, 2, retries)


def nodes_in_full_tree(levels: int) -> int:
    """A tree where every node has 2 children: 1 + 2 + 4 + ... over `levels` levels = 2^levels - 1."""
    return 2 ** levels - 1


# ------------------------------------------------------------------ logarithms
def floor_log2(n: int) -> int:
    """Largest k with 2^k <= n (for n >= 1): one less than the number of bits."""
    if n < 1:
        raise ValueError("n must be at least 1")
    return n.bit_length() - 1


def ceil_log2(n: int) -> int:
    """Smallest k with 2^k >= n (for n >= 1)."""
    if n < 1:
        raise ValueError("n must be at least 1")
    return (n - 1).bit_length()


def halvings_until_one(n: int) -> int:
    """Count halvings (rounding down) until 1 - equals floor_log2(n)."""
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


def tournament_rounds(players: int) -> int:
    """Rounds in a knockout tournament (byes allowed): ceiling of log2(players)."""
    return ceil_log2(players)


def decimal_digits(n: int) -> int:
    """Digits of a positive whole number = floor(log10 n) + 1 (computed exactly with integers)."""
    if n < 1:
        raise ValueError("n must be at least 1")
    digits = 0
    while n:
        n //= 10
        digits += 1
    return digits


def log_base(x: float, base: float) -> float:
    """Change of base: log_b(x) = ln(x) / ln(b)."""
    return math.log(x) / math.log(base)


def years_to_double(rate_percent: float) -> float:
    """Exact doubling time for compound growth: log(2) / log(1 + r)."""
    return math.log(2) / math.log(1 + rate_percent / 100)


def harmonic(n: int) -> float:
    """1 + 1/2 + 1/3 + ... + 1/n, which grows like ln(n)."""
    return sum(1 / k for k in range(1, n + 1))


if __name__ == "__main__":
    print("1..100 by loop and formula:", sum_loop(1, 100), arithmetic_sum(1, 100, 100))
    print("Bus fares 15, 20, ..., 60 (10 fares):", arithmetic_sum(15, 60, 10), sum_loop(15, 60, 5))
    print("Sum of squares 1..10:", sum_of_squares(10))
    print("1 + 2 + 4 + ... + 512:", geometric_sum(1, 2, 10), geometric_sum_loop(1, 2, 10))
    print("1 + 1/2 + 1/4 + ... (20 terms):", round(geometric_sum(1, 0.5, 20), 6))
    print("Chessboard grains:", f"{chessboard_grains():,}")
    print("Total wait for 6 retries:", total_backoff_wait(6), "seconds")
    print("Nodes in a full tree of 10 levels:", nodes_in_full_tree(10))
    print("floor/ceil log2 of 1000:", floor_log2(1000), ceil_log2(1000), "| halvings:", halvings_until_one(1000))
    print("Rounds for 100 players:", tournament_rounds(100), "| digits in 2^100:", decimal_digits(2 ** 100))
    print("log base 10 of 1000:", round(log_base(1000, 10), 6))
    print("Years to double at 7%:", round(years_to_double(7), 2), "| rule of 72 says", round(72 / 7, 2))
    print("Harmonic(1000) vs ln(1000):", round(harmonic(1000), 3), round(math.log(1000), 3))
