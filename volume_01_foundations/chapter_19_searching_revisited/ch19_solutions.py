"""Volume 1, Chapter 19, Thinking Problem 2 - count the different values by jumping over the copies.

A sorted list of n entries that holds only d different values is summarised as (value, copies) pairs with d upper-bound
searches, O(d log n), instead of walking all n entries.

Run:  python3 ch19_solutions.py
"""

from __future__ import annotations

from ch19_examples import CATALOGUE, upper_bound


def distinct_counts(a: list) -> list[tuple]:
    """(value, copies) for each different value of the sorted list a, using one upper bound per value."""
    result, i = [], 0
    while i < len(a):
        j = upper_bound(a, a[i])
        result.append((a[i], j - i))
        i = j
    return result


if __name__ == "__main__":
    print(distinct_counts(CATALOGUE))
