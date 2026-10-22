"""Volume 5, Chapter 20 - Thinking Problems.

Problem 1: for n = 2^k values, min_max makes exactly 3n/2 - 2 comparisons (checked).
Problem 2: the majority value (more than half) by divide and conquer, O(n log n).
Problem 3: min_max on an empty list used to recurse for ever; it now refuses the input.
"""

from __future__ import annotations


def majority(values: list):
    """A value occurring more than len/2 times, or None. A majority of the whole is a majority of some half."""
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    mid = len(values) // 2
    for cand in {majority(values[:mid]), majority(values[mid:])} - {None}:
        if values.count(cand) * 2 > len(values):
            return cand
    return None


if __name__ == "__main__":
    import ch20_examples as ex
    c = [0]
    ex.min_max(list(range(16)), c)
    print(c[0], 3 * 16 // 2 - 2, majority([3, 1, 3, 3, 2, 3, 3]), majority([1, 2, 3]))
