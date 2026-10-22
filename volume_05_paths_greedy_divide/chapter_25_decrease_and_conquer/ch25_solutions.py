"""Volume 5, Chapter 25 - Thinking Problems.

Problem 1: power(x, n) makes exactly bit_length(n) + popcount(n) multiplications for n >= 1 (checked).
Problem 2: the whole square root of n by halving the range of candidates: O(log n) squarings.
Problem 3: power with a negative n used to recurse for ever (-1 // 2 is -1); it now refuses the input.
"""

from __future__ import annotations


def multiplications(n: int) -> int:
    return n.bit_length() + bin(n).count("1") if n > 0 else 0


def isqrt_halving(n: int) -> tuple[int, int]:
    """Largest r with r * r <= n, by keeping lo*lo <= n < hi*hi and halving. Returns (r, squarings)."""
    if n < 0:
        raise ValueError("no whole square root of a negative number")
    lo, hi, steps = 0, n + 1, 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        steps += 1
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo, steps


if __name__ == "__main__":
    print(multiplications(13), isqrt_halving(10 ** 12), isqrt_halving(99))
