"""Volume 5, Chapter 26 - Thinking Problems.

Problem 1: Horner's rule computes c0 x^k + ... + ck (checked against the direct sum).
Problem 2: is there a pair of values differing by exactly d? Sort, then walk two pointers: O(n log n).
Problem 3: feeding the coefficients lowest first evaluates a different polynomial: [1, 2, 3] at 10 gives 123, not 321.
"""

from __future__ import annotations

from ch26_examples import horner


def pair_with_difference(values: list, d: int):
    """A pair (a, b) from values with b - a = d (d >= 0, different positions), or None."""
    if d < 0:
        d = -d
    s = sorted(values)
    i, j = 0, 1
    while j < len(s):
        gap = s[j] - s[i]
        if i != j and gap == d:
            return s[i], s[j]
        if gap < d:
            j += 1
        else:
            i += 1
            if i == j:
                j += 1
    return None


def horner_low_first(coeffs: list, x) -> float:
    """The mistake: coefficients given lowest power first, but used as if highest first."""
    total = 0
    for c in coeffs:
        total = total * x + c
    return total


if __name__ == "__main__":
    print(pair_with_difference([58, 25, 91, 12, 70, 47, 84, 31, 63], 23), pair_with_difference([1, 5, 9], 3))
    print(horner([3, 2, 1], 10, [0]), horner_low_first([1, 2, 3], 10))
