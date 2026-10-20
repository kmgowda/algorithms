"""Volume 1, Chapter 3 - Writing Algorithms Down.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


def shelf_for(call_number: int) -> str:
    """The return-desk rule of Figure 3.3: below 30 -> A, 30 to 59 -> B, 60 and up -> C."""
    if call_number < 30:
        return "A"
    elif call_number < 60:
        return "B"
    else:
        return "C"


def count_above(shelf: list[int], limit: int) -> int:
    """How many call numbers on the shelf are greater than limit (Figure 3.4)."""
    count = 0
    for book in shelf:
        if book > limit:
            count = count + 1
    return count


def halving_rounds(books: int) -> int:
    """How many times `books` can be halved (rounding down) until one is left (Figure 3.5)."""
    rounds = 0
    while books > 1:
        books = books // 2
        rounds = rounds + 1
    return rounds


def late_fee(days_late: int) -> int:
    """Fee in cents: the first 2 days are free, then 10 cents a day, never more than 100 (Figure 3.6)."""
    if days_late <= 2:
        return 0
    return min((days_late - 2) * 10, 100)


def swap(a, b):
    """Exchange two values with a spare, as in Figure 3.2; returns the new (a, b)."""
    temp = a
    a = b
    b = temp
    return a, b


if __name__ == "__main__":
    print([shelf_for(n) for n in (29, 30, 59, 60, 63)])
    print(count_above(SHELF, 50), count_above(SHELF, 60), halving_rounds(9), halving_rounds(100))
    print(late_fee(4), late_fee(12), late_fee(2), late_fee(13), swap("juice", "milk"))
