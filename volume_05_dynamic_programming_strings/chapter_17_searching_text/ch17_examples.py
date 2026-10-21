"""Volume 5, Chapter 17 - Searching Text: the straightforward way, and when it is slow.

Run:  python3 ch17_examples.py
"""

from __future__ import annotations

NEWSLETTER = "the reading club meets on monday; the club reads maps and poems at the library"


def naive_search(text: str, pattern: str) -> tuple[list, int]:
    """Try the pattern at every position, comparing letter by letter until a mismatch (Figure 17.2).
    Returns (positions where it occurs, letter comparisons)."""
    found, comparisons = [], 0
    n, m = len(text), len(pattern)
    for s in range(n - m + 1):
        k = 0
        while k < m:
            comparisons += 1
            if text[s + k] != pattern[k]:
                break
            k += 1
        if k == m:
            found.append(s)
    return found, comparisons


if __name__ == "__main__":
    print(naive_search(NEWSLETTER, "club"))
    print(naive_search(NEWSLETTER, "poems"), naive_search(NEWSLETTER, "opera"))
    t = "a" * 1000
    print(naive_search(t, "a" * 9 + "b")[1], naive_search(t, "b" + "a" * 9)[1], naive_search(t, "aaa")[0][:3], len(naive_search(t, "aaa")[0]))
    import random
    r = random.Random(17)
    rt = "".join(r.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(10000))
    print(naive_search(rt, "library")[1])
