"""Volume 6, Chapter 26 - Thinking Problems.

Problem 1: KMP makes at most 2n - 1 letter comparisons on a text of n letters (checked).
Problem 2: the shortest repeating unit of a string from its failure table: p = n - fail[n - 1].
Problem 3: resetting to 0 after a match, instead of to fail[k - 1], misses overlapping occurrences.
"""

from __future__ import annotations

from ch26_examples import failure


def shortest_period(s: str) -> str:
    """The shortest u with s = u repeated a whole number of times."""
    if not s:
        return ""
    p = len(s) - failure(s)[-1]
    return s[:p] if len(s) % p == 0 else s


def kmp_reset_bug(text: str, pattern: str) -> list:
    fail, found, k = failure(pattern), [], 0
    for i, ch in enumerate(text):
        while k and ch != pattern[k]:
            k = fail[k - 1]
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            found.append(i - k + 1)
            k = 0                                      # the bug: forgets the overlap
    return found


if __name__ == "__main__":
    from ch26_examples import kmp_search
    print(shortest_period("abcabcabc"), shortest_period("abab a"), shortest_period("aaaa"))
    print(kmp_reset_bug("AAAA", "AAA"), kmp_search("AAAA", "AAA")[0], kmp_reset_bug("ABABAB", "ABAB"))
