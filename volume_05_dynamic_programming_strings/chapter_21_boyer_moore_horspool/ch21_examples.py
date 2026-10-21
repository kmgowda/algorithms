"""Volume 5, Chapter 21 - Boyer-Moore-Horspool: compare from the right end, and jump ahead on a mismatch.

Run:  python3 ch21_examples.py
"""

from __future__ import annotations

import random


def shift_table(pattern: str) -> dict:
    """How far to slide when the text letter under the pattern's last position is ch (Figure 21.2)."""
    m = len(pattern)
    return {ch: m - 1 - i for i, ch in enumerate(pattern[:-1])}


def horspool(text: str, pattern: str) -> tuple[list, int, int]:
    """Returns (positions, letter comparisons, shifts tried)."""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1)), 0, 0
    table, found, comparisons, tries = shift_table(pattern), [], 0, 0
    s = 0
    while s <= n - m:
        tries += 1
        k = m - 1
        while k >= 0:
            comparisons += 1
            if text[s + k] != pattern[k]:
                break
            k -= 1
        if k < 0:
            found.append(s)
        s += table.get(text[s + m - 1], m)            # a letter not in the pattern: jump the whole length
    return found, comparisons, tries


NEWSLETTER = "the reading club meets on monday; the club reads maps and poems at the library"

if __name__ == "__main__":
    print(shift_table("club"), shift_table("poems"), shift_table("aaab"))
    print(horspool(NEWSLETTER, "club"), horspool(NEWSLETTER, "library"))
    r = random.Random(21)
    t = "".join(r.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(10000))
    for p in ("library", "reading club", "a"):
        print(p, horspool(t, p)[1:])
    print(horspool("a" * 1000, "a" * 9 + "b")[1:], horspool("a" * 1000, "b" + "a" * 9)[1:])
