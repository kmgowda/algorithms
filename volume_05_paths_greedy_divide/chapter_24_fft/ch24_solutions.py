"""Volume 5, Chapter 24 - Thinking Problems.

Problem 1: squaring the 2n-th roots of unity gives each n-th root exactly twice (the halving lemma; checked).
Problem 2: how many ways can one book from each of two shelves add up to each total? Multiply two polynomials.
Problem 3: forgetting to pad wraps the product round: [1, 1, 1, 1] squared with 4 points gives [4, 4, 4, 4].
"""

from __future__ import annotations

from ch24_examples import fft, fft_multiply, roots_of_unity


def squared_roots_match(n: int) -> bool:
    big, small = roots_of_unity(2 * n), roots_of_unity(n)
    return all(abs(big[k] ** 2 - small[k % n]) < 1e-9 for k in range(2 * n))


def pair_sum_counts(prices_a: list, prices_b: list) -> dict:
    """total -> number of (a, b) pairs, one price from each shelf, adding to it (whole-pound prices >= 0)."""
    if not prices_a or not prices_b:
        return {}
    pa, pb = [0] * (max(prices_a) + 1), [0] * (max(prices_b) + 1)
    for p in prices_a:
        pa[p] += 1
    for p in prices_b:
        pb[p] += 1
    return {t: c for t, c in enumerate(fft_multiply(pa, pb)) if c}


def unpadded_square(a: list) -> list:
    """The bug: transform with exactly len(a) points, so the high coefficients wrap round to the low ones."""
    n = len(a)
    fa = fft(a)
    back = fft([v * v for v in fa], invert=True)
    return [round((v / n).real) for v in back]


if __name__ == "__main__":
    print(squared_roots_match(8), pair_sum_counts([3, 5, 5, 8], [2, 4, 7]))
    print(unpadded_square([1, 1, 1, 1]), fft_multiply([1, 1, 1, 1], [1, 1, 1, 1]))
