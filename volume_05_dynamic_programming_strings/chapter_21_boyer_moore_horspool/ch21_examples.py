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


def good_suffix_table(pattern: str) -> list:
    """The good-suffix rule (Section 21.6). shift[j], for j = 1..m, is how far to slide when the last m - j letters
    of the pattern have matched and the letter before them failed; shift[0] is the slide after a full match.
    It slides to the next place where the matched ending occurs again in the pattern with a different letter
    before it, or, failing that, to where the longest border of the pattern lines up with the text."""
    m = len(pattern)
    shift, border = [0] * (m + 1), [0] * (m + 1)
    i, j = m, m + 1
    border[i] = j
    while i > 0:                                       # pass 1: matched endings that recur inside the pattern
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = border[j]
        i, j = i - 1, j - 1
        border[i] = j
    j = border[0]
    for i in range(m + 1):                             # pass 2: otherwise line up the pattern's borders
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = border[j]
    return shift


def boyer_moore(text: str, pattern: str) -> tuple[list, int, int]:
    """Full Boyer-Moore: compare right to left; on a mismatch slide by the larger of the bad-character rule
    (line the failing text letter up with its last appearance to the left in the pattern) and the good-suffix rule.
    Returns (positions, letter comparisons, shifts tried)."""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1)), 0, 0
    last = {ch: i for i, ch in enumerate(pattern)}    # last position of each letter in the pattern
    good = good_suffix_table(pattern)
    found, comparisons, tries, s = [], 0, 0, 0
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
            s += good[0]
        else:
            bad = k - last.get(text[s + k], -1)
            s += max(bad, good[k + 1], 1)
    return found, comparisons, tries


def random_text(n: int = 10000, seed: int = 30) -> str:
    """The shared random text of Part II (the same as Chapters 17, 19 and 30)."""
    r = random.Random(seed)
    return "".join(r.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(n))


NEWSLETTER = "the reading club meets on monday; the club reads maps and poems at the library"

if __name__ == "__main__":
    print(shift_table("club"), shift_table("poems"), shift_table("aaab"))
    print(horspool(NEWSLETTER, "club"), horspool(NEWSLETTER, "library"))
    t = random_text()
    for p in ("library", "reading club", "a"):
        print(p, horspool(t, p)[1:])
    print(horspool("a" * 1000, "a" * 9 + "b")[1:], horspool("a" * 1000, "b" + "a" * 9)[1:])
