"""Volume 1, Chapter 4 - Lists, Arrays, and Dictionaries.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]
TITLES = {63: "Maps of the World", 12: "First Steps in Python", 84: "Ocean Life", 31: "Clocks and Calendars"}


def address_of(start: int, index: int) -> int:
    """Where item `index` of an array starting at `start` lives (Figure 4.1)."""
    return start + index


def insert_sorted(shelf: list[int], new: int) -> int:
    """Insert `new` into the sorted list `shelf` by shifting larger items right (Figure 4.2).
    Returns how many items were shifted."""
    shelf.append(new)                 # make room at the end
    i = len(shelf) - 2
    while i >= 0 and shelf[i] > new:
        shelf[i + 1] = shelf[i]       # shift one place right
        i = i - 1
    shelf[i + 1] = new
    return len(shelf) - 2 - i


def remove_at(shelf: list[int], index: int) -> int:
    """Remove the item at `index` by shifting later items left (Figure 4.3). Returns the number of shifts."""
    shifts = 0
    for i in range(index, len(shelf) - 1):
        shelf[i] = shelf[i + 1]
        shifts += 1
    shelf.pop()
    return shifts


def copies_while_appending(items: int, capacity: int = 1) -> int:
    """How many whole-block copies happen when appending `items` to a list that doubles when full (Figure 4.4)."""
    size, copies = 0, 0
    for _ in range(items):
        if size == capacity:
            capacity *= 2
            copies += 1
        size += 1
    return copies


if __name__ == "__main__":
    s = SHELF[:]
    print(insert_sorted(s, 40), s)
    s = SHELF[:]
    print(remove_at(s, 2), s)
    print(address_of(1000, 7), copies_while_appending(9), TITLES[63])
