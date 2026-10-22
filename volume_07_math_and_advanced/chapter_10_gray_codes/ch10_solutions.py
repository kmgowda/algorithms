"""Volume 7, Chapter 10 - Thinking Problems.

Problem 1: gray(k - 1) and gray(k) differ in exactly the bit at the position of the lowest 1 bit of k (checked).
Problem 2: the total weight of every subset, in Gray order, with one addition or subtraction per subset.
Problem 3: decoding with a single XOR, g ^ (g >> 1), is wrong; the first failure is g = 4.
"""

from __future__ import annotations

from ch10_examples import from_gray, gray


def subset_totals_gray(weights: list) -> list:
    """(mask, total) for all 2^n subsets, in Gray order: each step adds or removes exactly one item."""
    mask, total, out = 0, 0, [(0, 0)]
    for k in range(1, 1 << len(weights)):
        i = (k & -k).bit_length() - 1          # the one item that changes
        if mask >> i & 1:
            total -= weights[i]
        else:
            total += weights[i]
        mask ^= 1 << i
        out.append((mask, total))
    return out


def wrong_from_gray(g: int) -> int:
    return g ^ (g >> 1)


def first_wrong_decode(limit: int = 1 << 12) -> int | None:
    return next((g for g in range(limit) if wrong_from_gray(g) != from_gray(g)), None)


if __name__ == "__main__":
    print(subset_totals_gray([3, 5, 9]))
    print(first_wrong_decode(), wrong_from_gray(4), from_gray(4), gray(7))
