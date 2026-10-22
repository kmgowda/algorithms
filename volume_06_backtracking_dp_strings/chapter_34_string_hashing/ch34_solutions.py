"""Volume 6, Chapter 34 - Thinking Problems.

Problem 1: get(a, b) = h[b] - h[a] * BASE^(b - a) is exactly the hash of s[a:b] computed from scratch (checked).
Problem 2: the longest common prefix of two suffixes in O(log n) hash comparisons, by binary search on its length.
Problem 3: comparing hashes without comparing lengths: a letter with code 0 in front leaves the hash unchanged.
"""

from __future__ import annotations

from ch34_examples import BASE, MOD, PrefixHash


def direct_hash(s: str, base: int = BASE, mod: int = MOD) -> int:
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % mod
    return h


def lcp_by_hash(ph: PrefixHash, n: int, i: int, j: int) -> int:
    lo, hi = 0, n - max(i, j)                         # the first lo letters agree
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ph.get(i, i + mid) == ph.get(j, j + mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def same_no_length(s: str, a: int, b: int, c: int, d: int) -> bool:
    ph = PrefixHash(s)
    return ph.get(a, b) == ph.get(c, d)               # the bug: lengths not compared


if __name__ == "__main__":
    s = "the club reads, the club meets"
    ph = PrefixHash(s)
    print(lcp_by_hash(ph, len(s), 0, 16), same_no_length("\0a", 0, 2, 1, 2), "\0a"[0:2] == "\0a"[1:2])
