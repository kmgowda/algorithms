"""Volume 1, Chapter 6, Thinking Problem 2 - finding a duplicate call number in about n + K steps.

Run:  python3 ch06_solutions.py
"""

from __future__ import annotations


def has_duplicate(books: list[int], largest: int) -> bool:
    """Does any call number appear twice? Every call number is between 0 and largest.

    seen[v] records whether call number v has been met already, so each book needs one look at the shelf and
    one look at seen, instead of a comparison with every other book."""
    seen = [False] * (largest + 1)
    for b in books:
        if seen[b]:
            return True
        seen[b] = True
    return False


def hidden_comparisons(books: list[int]) -> int:
    """Comparisons made by "if b not in result: append b" (Thinking Problem 3): the "in" test is a linear search
    of result, so it compares b with every book kept so far when b is new."""
    result: list[int] = []
    count = 0
    for b in books:
        for kept in result:
            count += 1
            if kept == b:
                break
        else:
            result.append(b)
    return count


if __name__ == "__main__":
    shelf = [12, 25, 31, 47, 58, 63, 70, 84, 91]
    print(has_duplicate(shelf, 100), has_duplicate(shelf + [47], 100))
    print([hidden_comparisons(list(range(n))) for n in (1000, 2000)])
