"""Volume 5, Chapter 18 - Knuth-Morris-Pratt: never look at a text letter twice.

Run:  python3 ch18_examples.py
"""

from __future__ import annotations


def failure(pattern: str) -> list:
    """fail[k] = length of the longest proper prefix of pattern[:k+1] that is also a suffix of it (Figure 18.2)."""
    fail, k = [0] * len(pattern), 0
    for i in range(1, len(pattern)):
        while k and pattern[i] != pattern[k]:
            k = fail[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        fail[i] = k
    return fail


def kmp_search(text: str, pattern: str) -> tuple[list, int]:
    """Every occurrence of pattern, with letter comparisons counted (Figure 18.3). Empty pattern: every position."""
    if not pattern:
        return list(range(len(text) + 1)), 0
    fail, found, k, comparisons = failure(pattern), [], 0, 0
    for i, ch in enumerate(text):
        while True:
            comparisons += 1
            if ch == pattern[k]:
                k += 1
                break
            if k == 0:
                break
            k = fail[k - 1]                           # slide the pattern; keep the part already known to match
        if k == len(pattern):
            found.append(i - k + 1)
            k = fail[k - 1]
    return found, comparisons


if __name__ == "__main__":
    print(failure("abacab"), failure("aaaab"), failure("abcd"))
    print(kmp_search("abacabacab", "abacab"))
    t = "a" * 1000
    print(kmp_search(t, "a" * 9 + "b")[1], kmp_search(t, "b" + "a" * 9)[1], len(kmp_search(t, "aaa")[0]))
    nl = "the reading club meets on monday; the club reads maps and poems at the library"
    print(kmp_search(nl, "club"))
