"""Volume 1, Chapter 4, Thinking Problem 2 - shelving a whole sorted batch of new books at once.

Instead of calling insert_sorted once per new book (up to n shifts each), fill the enlarged shelf from
the back: the larger of the last unplaced shelf book and the last unplaced new book goes into the last
free cell. Every book is written at most once, so at most n + m writes in all.

Run:  python3 ch04_solutions.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


def insert_batch(shelf: list[int], batch: list[int]) -> int:
    """Insert the sorted list `batch` into the sorted list `shelf`, filling from the back.
    Returns how many cells were written."""
    i, j = len(shelf) - 1, len(batch) - 1
    shelf.extend(batch)               # make room for len(batch) more books
    k = len(shelf) - 1
    writes = 0
    while j >= 0:
        if i >= 0 and shelf[i] > batch[j]:
            shelf[k] = shelf[i]       # an old book moves to its final cell
            i = i - 1
        else:
            shelf[k] = batch[j]       # a new book goes into its final cell
            j = j - 1
        k = k - 1
        writes = writes + 1
    return writes


def items_copied_growing_by(items: int, step: int) -> int:
    """Thinking Problem 1: items copied while appending, when a full list grows by `step` cells
    (starting with room for `step`)."""
    size, capacity, copied = 0, step, 0
    for _ in range(items):
        if size == capacity:
            capacity += step
            copied += size
        size += 1
    return copied


if __name__ == "__main__":
    s = SHELF[:]
    print(insert_batch(s, [40, 60, 95]), s)
    print(items_copied_growing_by(1000, 10), items_copied_growing_by(10_000, 10))
