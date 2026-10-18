"""Volume 13, Chapter 4 - Knuth-Morris-Pratt: Never Look Back.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations


def prefix_function(pattern: str) -> list[int]:
    """pi[i] = length of the longest proper prefix of pattern[:i+1] that is also a suffix of it.
    After a mismatch, pi tells how much of the pattern is STILL matched - so the text is never re-read."""
    pi = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k and pattern[i] != pattern[k]:
            k = pi[k - 1]                          # fall back to the next shorter border
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k
    return pi


def kmp_search(text: str, pattern: str) -> tuple[list[int], int]:
    """All occurrences in O(n + m). Returns (occurrences, character comparisons in the search phase)."""
    if not pattern:
        return [0], 0
    pi = prefix_function(pattern)
    found, k, comparisons = [], 0, 0
    for i, ch in enumerate(text):
        while k and ch != pattern[k]:
            comparisons += 1
            k = pi[k - 1]
        comparisons += 1
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            found.append(i - k + 1)
            k = pi[k - 1]                          # keep going: overlaps allowed
    return found, comparisons


def naive_comparisons(text: str, pattern: str) -> int:
    """For comparison: character comparisons made by naive matching (Chapter 2)."""
    count = 0
    for i in range(len(text) - len(pattern) + 1):
        for j in range(len(pattern)):
            count += 1
            if text[i + j] != pattern[j]:
                break
    return count


def stream_alarm(chunks: list[str], signature: str) -> list[int]:
    """Industry example: scan a network stream arriving in chunks for a signature, keeping only the KMP state
    between chunks - matches spanning chunk boundaries are still found. Returns global start positions."""
    pi = prefix_function(signature)
    k, pos, hits = 0, 0, []
    for chunk in chunks:
        for ch in chunk:
            while k and ch != signature[k]:
                k = pi[k - 1]
            if ch == signature[k]:
                k += 1
            if k == len(signature):
                hits.append(pos - k + 1)
                k = pi[k - 1]
            pos += 1
    return hits


if __name__ == "__main__":
    print(prefix_function("ababaca"), prefix_function("aabaaab"))
    print(kmp_search("abababa", "aba"))
    t, p = "a" * 10000, "a" * 49 + "b"
    print("worst case: KMP", kmp_search(t, p)[1], "comparisons vs naive", naive_comparisons(t, p))
    print("stream:", stream_alarm(["GET /ind", "ex.html?id=1 UNI", "ON SELECT pass"], "UNION SELECT"))
