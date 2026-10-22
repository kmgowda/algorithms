"""Volume 1, Chapter 5, Thinking Problem 2 - the smallest and the largest together, in about 3n/2 comparisons.

Run:  python3 ch05_solutions.py
"""

from __future__ import annotations


def min_and_max(values: list[int]) -> tuple[int, int, int]:
    """Smallest and largest of a non-empty list, plus the number of comparisons made.

    The items are taken in pairs: the two items of a pair are compared with each other first, then only the
    smaller one can be a new smallest and only the larger one a new largest. That is 3 comparisons for every
    2 items, instead of 4 when each item is tested against both the smallest and the largest so far."""
    n = len(values)
    comparisons = 0
    if n % 2 == 1:
        least = best = values[0]
        i = 1
    else:
        comparisons += 1
        if values[0] > values[1]:
            least, best = values[1], values[0]
        else:
            least, best = values[0], values[1]
        i = 2
    while i + 1 < n:
        comparisons += 3
        if values[i] > values[i + 1]:
            small, big = values[i + 1], values[i]
        else:
            small, big = values[i], values[i + 1]
        if small < least:
            least = small
        if big > best:
            best = big
        i = i + 2
    return least, best, comparisons


if __name__ == "__main__":
    visits = [34, 41, 29, 56, 48, 61, 22]
    print(min_and_max(visits))
