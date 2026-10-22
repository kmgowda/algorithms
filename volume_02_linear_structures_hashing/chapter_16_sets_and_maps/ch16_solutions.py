"""Volume 2, Chapter 16 - Thinking Problems.

Problem 2: list titles from most to least borrowed in O(n), with count buckets instead of a sort.
Problem 3: the shared-list bug of dict.fromkeys(keys, []), kept here so the tests can show it.
"""

from __future__ import annotations


def titles_by_popularity(loans: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    for title in loans:
        counts[title] = counts.get(title, 0) + 1
    buckets: list[list[str]] = [[] for _ in range(len(loans) + 1)]
    for title, c in counts.items():          # a dict keeps first-appearance order
        buckets[c].append(title)
    return [t for c in range(len(loans), 0, -1) for t in buckets[c]]


def group_by_author_buggy(books: list[tuple[str, str]]) -> dict[str, list[str]]:
    """WRONG: every author shares one list, so every author gets every title."""
    shelves = dict.fromkeys((author for author, _ in books), [])
    for author, title in books:
        shelves[author].append(title)
    return shelves


if __name__ == "__main__":
    print(titles_by_popularity(["Maps", "Ocean", "Maps", "Clocks", "Maps", "Ocean"]))
    print(group_by_author_buggy([("Lucas", "Hanoi"), ("Polya", "How to Solve It")]))
