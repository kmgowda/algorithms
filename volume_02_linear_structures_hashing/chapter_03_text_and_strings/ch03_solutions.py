"""Volume 2, Chapter 3 - Thinking Problems.

Problem 1: a word whose letters are all different has matches at least its length apart (checked in the tests).
Problem 2: is word a subsequence of text? One pass with two pointers, O(n + m).
Problem 3: the "skip past what was compared" search, kept here so the tests can show it misses matches.
"""

from __future__ import annotations


def is_subsequence(word: str, text: str) -> bool:
    """True if word's letters appear in text in order, gaps allowed: each text letter is read once."""
    k = 0
    for ch in text:
        if k < len(word) and ch == word[k]:
            k += 1
    return k == len(word)


def find_all_skipping(text: str, word: str) -> list[int]:
    """WRONG: after comparing k + 1 letters at a start, jumps k + 1 places, so it can step over a match."""
    matches, start, m = [], 0, len(word)
    while m and start <= len(text) - m:
        k = 0
        while k < m and text[start + k] == word[k]:
            k += 1
        if k == m:
            matches.append(start)
            start += m
        else:
            start += k + 1
    return matches


if __name__ == "__main__":
    print(is_subsequence("LIAR", "LIBRARY"), is_subsequence("RAIL", "LIBRARY"), is_subsequence("", ""))
    print(find_all_skipping("CCAR", "CAR"), find_all_skipping("banana", "ana"), find_all_skipping("a map of maps", "map"))
