"""Volume 1, Chapter 1, Thinking Problem 2 - the shortest and the tallest child together.

Children are taken two at a time: the pair is compared once, then only its shorter child can be a new
shortest and only its taller child can be a new tallest. That costs at most 3 comparisons per pair
instead of 4, about 3n/2 comparisons in all instead of 2n - 2.

Run:  python3 ch01_solutions.py
"""

from __future__ import annotations

HEIGHTS = [142, 155, 138, 161, 150, 158]


def shortest_and_tallest(heights: list[int]) -> tuple[int, int, int]:
    """Return (shortest, tallest, comparisons made) for a non-empty list, comparing children in pairs."""
    n = len(heights)
    comparisons = 0
    if n % 2 == 1:
        shortest = tallest = heights[0]
        start = 1
    else:
        comparisons += 1
        if heights[0] < heights[1]:
            shortest, tallest = heights[0], heights[1]
        else:
            shortest, tallest = heights[1], heights[0]
        start = 2
    for i in range(start, n - 1, 2):
        a, b = heights[i], heights[i + 1]
        comparisons += 1
        if a > b:
            a, b = b, a                    # now a is the shorter of the pair
        comparisons += 2
        if a < shortest:
            shortest = a
        if b > tallest:
            tallest = b
    return shortest, tallest, comparisons


if __name__ == "__main__":
    print(shortest_and_tallest(HEIGHTS))
    for n in range(1, 11):
        print(n, shortest_and_tallest(list(range(n)))[2])
