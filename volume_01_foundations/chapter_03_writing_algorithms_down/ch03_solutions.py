"""Volume 1, Chapter 3, Thinking Problem 2 - the two closest call numbers on a sorted shelf.

On a sorted shelf the closest pair of books always stands side by side, so one loop over the n - 1
neighbouring pairs replaces the loop inside a loop of Practice Problem 3 (n(n - 1)/2 pairs).

Run:  python3 ch03_solutions.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


def smallest_gap(shelf: list[int]) -> tuple[int, int, int] | None:
    """For a sorted shelf, return (gap, left book, right book) for the closest pair of neighbours,
    or None when the shelf has fewer than two books. Makes len(shelf) - 1 subtractions."""
    if len(shelf) < 2:
        return None
    best = (shelf[1] - shelf[0], shelf[0], shelf[1])
    for i in range(1, len(shelf) - 1):
        gap = shelf[i + 1] - shelf[i]
        if gap < best[0]:
            best = (gap, shelf[i], shelf[i + 1])
    return best


if __name__ == "__main__":
    print(smallest_gap(SHELF))
