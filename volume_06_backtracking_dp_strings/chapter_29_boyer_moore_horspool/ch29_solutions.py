"""Volume 6, Chapter 29 - Thinking Problems.

Problem 1: Horspool's slide never skips an occurrence (checked against a plain search on random texts).
Problem 2: Sunday's variant looks at the letter just after the window and may slide m + 1 places.
Problem 3: building the shift table from the whole pattern gives the last letter a slide of 0: the search stalls.
"""

from __future__ import annotations


def sunday(text: str, pattern: str) -> tuple[list, int]:
    """Returns (positions, windows tried)."""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1)), 0
    shift = {ch: m - i for i, ch in enumerate(pattern)}       # later positions overwrite earlier ones
    s, found, tries = 0, [], 0
    while s <= n - m:
        tries += 1
        if text[s:s + m] == pattern:
            found.append(s)
        if s + m >= n:
            break
        s += shift.get(text[s + m], m + 1)
    return found, tries


def horspool_whole_table(text: str, pattern: str, limit: int = 1000) -> tuple[list, int]:
    """The bug: the table includes the pattern's last letter, so its slide is 0. Stops after `limit` tries."""
    m = len(pattern)
    table = {ch: m - 1 - i for i, ch in enumerate(pattern)}
    s, found, tries = 0, [], 0
    while s <= len(text) - m and tries < limit:
        tries += 1
        if text[s:s + m] == pattern and s not in found:
            found.append(s)
        s += table.get(text[s + m - 1], m)
    return found, tries


if __name__ == "__main__":
    from ch29_examples import NEWSLETTER, horspool
    print(horspool(NEWSLETTER, "library")[2], sunday(NEWSLETTER, "library"), horspool(NEWSLETTER, "library")[0])
    print(horspool_whole_table("the club", "club"), horspool_whole_table("xbab", "ab"))
