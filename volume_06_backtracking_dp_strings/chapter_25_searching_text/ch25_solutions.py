"""Volume 6, Chapter 25 - model solutions to the Thinking Problems (Section 25.14)."""

from __future__ import annotations


def wildcard_search(text: str, pattern: str, wild: str = "?") -> tuple[list, int]:
    """Occurrences of a pattern in which the wildcard matches any one letter. Only the pattern's real letters
    are compared, in order, so on random text the cost stays near one comparison per shift.
    Returns (positions, letter comparisons)."""
    n, m = len(text), len(pattern)
    checks = [k for k, ch in enumerate(pattern) if ch != wild]
    found, comparisons = [], 0
    for s in range(n - m + 1):
        for k in checks:
            comparisons += 1
            if text[s + k] != pattern[k]:
                break
        else:
            found.append(s)
    return found, comparisons


def skip_ahead_bug(text: str, pattern: str, extra: int = 1) -> list:
    """Thinking Problem 3's bug: after failing at letter k, jump to shift s + k + extra (extra = 1 or 0)."""
    n, m = len(text), len(pattern)
    found, s = [], 0
    while s <= n - m:
        k = 0
        while k < m and text[s + k] == pattern[k]:
            k += 1
        if k == m:
            found.append(s)
            s += 1
        else:
            s += max(1, k + extra)
    return found


def first_letter_bound_holds(text: str, pattern: str) -> bool:
    """Thinking Problem 1: if pattern[0] occurs nowhere else in the pattern, the naive search makes <= 2n."""
    from ch25_examples import naive_search
    return naive_search(text, pattern)[1] <= 2 * len(text)


if __name__ == "__main__":
    from ch25_examples import NEWSLETTER, naive_search, random_text
    rt = random_text()
    found, c = wildcard_search(rt, "???????y")
    print(len(found), c, naive_search(rt.replace("?", "#"), "???????y")[1])
    print(skip_ahead_bug("aab", "ab"), skip_ahead_bug("aaab", "aab", 0), naive_search(NEWSLETTER, "club"))
