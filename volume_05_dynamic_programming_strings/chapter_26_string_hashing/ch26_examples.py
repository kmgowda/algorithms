"""Volume 5, Chapter 26 - String Hashing in Practice: prefix hashes compare any two substrings in one step.

Run:  python3 ch26_examples.py
"""

from __future__ import annotations

import random

BASE, MOD = 131, (1 << 61) - 1


class PrefixHash:
    """h[i] = hash of s[:i]; the hash of s[a:b] is h[b] - h[a] * BASE^(b-a) (Figure 26.1)."""

    def __init__(self, s: str, base: int = BASE, mod: int = MOD):
        self.mod, self.h, self.p = mod, [0], [1]
        for ch in s:
            self.h.append((self.h[-1] * base + ord(ch)) % mod)
            self.p.append(self.p[-1] * base % mod)

    def get(self, a: int, b: int) -> int:
        return (self.h[b] - self.h[a] * self.p[b - a]) % self.mod


def same(s: str, a: int, b: int, c: int, d: int) -> bool:
    """Do s[a:b] and s[c:d] look equal by hash?"""
    ph = PrefixHash(s)
    return b - a == d - c and ph.get(a, b) == ph.get(c, d)


def distinct_of_length(s: str, k: int, mod: int = MOD) -> int:
    """Number of different k-letter substrings, counted by their hashes."""
    if k == 0:
        return 1
    ph = PrefixHash(s, mod=mod)
    return len({ph.get(i, i + k) for i in range(len(s) - k + 1)})


def longest_repeat(s: str) -> str:
    """Binary search on the length: is some length-L substring repeated? (hashes in a set)"""
    ph = PrefixHash(s)

    def repeated(L):
        seen = {}
        for i in range(len(s) - L + 1):
            h = ph.get(i, i + L)
            if h in seen and s[seen[h]:seen[h] + L] == s[i:i + L]:
                return i
            seen.setdefault(h, i)
        return -1

    lo, hi, at = 0, len(s) - 1, 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        i = repeated(mid)
        if i >= 0:
            lo, at = mid, i
        else:
            hi = mid - 1
    return s[at:at + lo] if lo > 0 else ""


def collisions(n_strings: int, mod: int, seed: int = 26) -> int:
    """How many pairs of different random 8-letter words share a hash, for a given modulus (Figure 26.3)."""
    r = random.Random(seed)
    words = {"".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(8)) for _ in range(n_strings)}
    seen, pairs = {}, 0
    for w in words:
        h = PrefixHash(w, mod=mod).get(0, len(w))
        pairs += seen.get(h, 0)
        seen[h] = seen.get(h, 0) + 1
    return pairs


if __name__ == "__main__":
    s = "the club reads; the club meets"
    print(same(s, 0, 8, 16, 24), same(s, 4, 8, 20, 24), same(s, 0, 3, 4, 7))
    print(distinct_of_length("banana", 2), distinct_of_length("banana", 3), longest_repeat("banana"), repr(longest_repeat(s)))
    for mod in (1000, 100_000, 10_000_000, MOD):
        print(mod, collisions(10_000, mod))
