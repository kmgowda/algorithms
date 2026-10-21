"""Volume 4, Chapter 22 - Decrease and Conquer: shrink the problem by one, by half, or by a variable amount.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations


def power(x: int, n: int, counter: list) -> int:
    """x to the n by halving n (Figure 22.2): about 2 log2 n multiplications instead of n - 1."""
    if n == 0:
        return 1
    half = power(x, n // 2, counter)
    counter[0] += 1
    result = half * half
    if n % 2:
        counter[0] += 1
        result *= x
    return result


def peasant(a: int, b: int, log: list | None = None) -> int:
    """Russian peasant multiplication (Figure 22.3): halve a, double b, add b whenever a is odd."""
    total = 0
    while a > 0:
        if log is not None:
            log.append((a, b, a % 2 == 1))
        if a % 2:
            total += b
        a, b = a // 2, b * 2
    return total


def guess_number(secret: int, low: int, high: int) -> int:
    """Guess a number in low..high by halving the range each time; returns the number of guesses."""
    guesses = 0
    while low <= high:
        guesses += 1
        mid = (low + high) // 2
        if mid == secret:
            return guesses
        if mid < secret:
            low = mid + 1
        else:
            high = mid - 1
    return guesses


def euclid(a: int, b: int, log: list | None = None) -> int:
    """Greatest common divisor: replace (a, b) by (b, a mod b); the size shrinks by a varying amount."""
    while b:
        if log is not None:
            log.append((a, b))
        a, b = b, a % b
    return a


if __name__ == "__main__":
    c = [0]
    print(power(3, 13, c), c[0], 3 ** 13)
    log = []
    print(peasant(13, 21, log), log)
    print(max(guess_number(s, 1, 1000) for s in range(1, 1001)))
    log = []
    print(euclid(1071, 462, log), log)
