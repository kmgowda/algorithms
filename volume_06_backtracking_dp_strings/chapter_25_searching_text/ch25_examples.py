"""Volume 6, Chapter 25 - Searching Text: the straightforward way, and when it is slow.

Run:  python3 ch25_examples.py
"""

from __future__ import annotations

NEWSLETTER = "the reading club meets on monday; the club reads maps and poems at the library"


def naive_search(text: str, pattern: str) -> tuple[list, int]:
    """Try the pattern at every position, comparing letter by letter until a mismatch (Figure 25.2).
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


ALPHABET = "abcdefghijklmnopqrstuvwxyz "


def random_text(n: int = 10000, seed: int = 30) -> str:
    """The shared random text of Part III (Chapters 25, 29 and 38): n letters and spaces, all equally likely."""
    import random
    r = random.Random(seed)
    return "".join(r.choice(ALPHABET) for _ in range(n))


def expected_comparisons(n: int, m: int, symbols: int = 27) -> float:
    """Average comparisons of the naive search on random text (Section 25.5): at each of the n - m + 1 shifts,
    comparison i + 1 happens only if the first i letters matched, which has chance (1/symbols)^i."""
    if m > n:
        return 0.0
    per_shift = sum((1 / symbols) ** i for i in range(m))
    return (n - m + 1) * per_shift


if __name__ == "__main__":
    print(naive_search(NEWSLETTER, "club"))
    print(naive_search(NEWSLETTER, "poems"), naive_search(NEWSLETTER, "opera"))
    t = "a" * 1000
    print(naive_search(t, "a" * 9 + "b")[1], naive_search(t, "b" + "a" * 9)[1], naive_search(t, "aaa")[0][:3], len(naive_search(t, "aaa")[0]))
    rt = random_text()
    print(naive_search(rt, "library")[1], round(expected_comparisons(10000, 7)))
