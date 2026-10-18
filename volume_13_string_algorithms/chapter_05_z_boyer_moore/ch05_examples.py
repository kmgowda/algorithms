"""Volume 13, Chapter 5 - Z-Algorithm and Boyer-Moore.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import random


def z_array(s: str) -> list[int]:
    """z[i] = length of the longest substring starting at i that matches a prefix of s.
    Keep the rightmost 'Z-box' [l, r) found so far; inside it, reuse earlier answers. O(n)."""
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])            # copy what the box already tells us
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1                              # extend by direct comparison
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def z_search(text: str, pattern: str, sep: str = "\x00") -> list[int]:
    """Search with Z: in pattern + sep + text, positions where z equals len(pattern) are matches."""
    m = len(pattern)
    z = z_array(pattern + sep + text)
    return [i - m - 1 for i in range(m + 1, len(z)) if z[i] >= m]


def horspool(text: str, pattern: str) -> tuple[list[int], int]:
    """Boyer-Moore-Horspool: compare RIGHT to LEFT; on any outcome, shift by how far the text letter under the
    pattern's last position is from the pattern's end (bad-character rule). Returns (occurrences, comparisons)."""
    n, m = len(text), len(pattern)
    if m == 0:
        return [0], 0
    shift = {ch: m - 1 - i for i, ch in enumerate(pattern[:-1])}   # last occurrence wins
    found, comparisons, i = [], 0, 0
    while i <= n - m:
        j = m - 1
        while j >= 0:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j -= 1
        if j < 0:
            found.append(i)
        i += shift.get(text[i + m - 1], m)
    return found, comparisons


def naive_comparisons(text: str, pattern: str) -> int:
    count = 0
    for i in range(len(text) - len(pattern) + 1):
        for j in range(len(pattern)):
            count += 1
            if text[i + j] != pattern[j]:
                break
    return count


def english_like(n: int, seed: int = 0) -> str:
    rng = random.Random(seed)
    words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", "river", "bank", "and", "sat"]
    out = []
    while sum(len(w) + 1 for w in out) < n:
        out.append(rng.choice(words))
    return " ".join(out)[:n]


def find_in_document(document: str, phrase: str) -> list[int]:
    """Industry example: an editor's find box - long phrases make Boyer-Moore skip most of the text."""
    return horspool(document, phrase)[0]


if __name__ == "__main__":
    print(z_array("aabxaab"), z_search("abacabadabacaba", "aba"))
    doc = english_like(20000) + " needle in a haystack"
    for p in ("dog", "lazy river bank", "needle in a haystack"):
        found, bm = horspool(doc, p)
        print(f"{p!r}: Horspool {bm} comparisons vs naive {naive_comparisons(doc, p)}")
    print(find_in_document("To be, or not to be, that is the question", "to be"))
