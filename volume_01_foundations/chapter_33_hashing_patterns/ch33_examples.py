"""Volume 1, Chapter 33 - Hashing Patterns.

Run:  python3 ch33_examples.py
"""

from __future__ import annotations

import random


def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    """Group words by their sorted letters (Figure 33.1)."""
    groups: dict[str, list[str]] = {}
    for w in words:
        groups.setdefault("".join(sorted(w)), []).append(w)
    return groups


def pair_for_card(prices: list[int], card: int) -> tuple[int, int] | None:
    """Two prices summing to card, in one pass with a set of prices seen so far (Figure 33.2)."""
    seen: set[int] = set()
    for p in prices:
        if card - p in seen:
            return card - p, p
        seen.add(p)
    return None


def first_unique(text: str) -> str | None:
    """The first character that appears exactly once: count, then scan (Figure 33.3)."""
    counts: dict[str, int] = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in text:
        if counts[ch] == 1:
            return ch
    return None


def dedupe(items: list) -> list:
    """Keep the first occurrence of each item, in order (Section 33.8)."""
    seen, out = set(), []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def leaderboard(log: list[tuple[str, str]], popular: int = 100):
    """Section 33.10: distinct books per reader, popular books, and double logs, in one pass."""
    books_of: dict[str, set[str]] = {}
    readers_of: dict[str, int] = {}
    doubles = []
    for reader, book in log:
        mine = books_of.setdefault(reader, set())
        if book in mine:
            doubles.append((reader, book))
            continue
        mine.add(book)
        readers_of[book] = readers_of.get(book, 0) + 1
    top = sorted(books_of, key=lambda r: (-len(books_of[r]), r))[:3]
    return top, sorted(b for b, c in readers_of.items() if c > popular), doubles


if __name__ == "__main__":
    print(group_anagrams(["listen", "silent", "enlist", "google", "inlets", "banana"]))
    print(pair_for_card([4, 9, 20, 6, 17, 13, 15], 30), pair_for_card([12, 18, 5, 25], 30), first_unique("SWISSCHEESE"),
          first_unique("LIBRARY"), dedupe([47, 12, 47, 63, 12, 91]))
    rng = random.Random(1)
    log = [(f"r{rng.randint(1, 800)}", f"b{rng.randint(1, 300)}") for _ in range(40_000)]
    top, pop, doubles = leaderboard(log)
    print(top, len(pop), len(doubles))
