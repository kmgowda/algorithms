"""Volume 6, Chapter 34 - String Hashing in Practice: prefix hashes compare any two substrings in one step.

Run:  python3 ch34_examples.py
"""

from __future__ import annotations

import random

BASE, MOD = 131, (1 << 61) - 1


class PrefixHash:
    """h[i] = hash of s[:i]; the hash of s[a:b] is h[b] - h[a] * BASE^(b-a) (Figure 34.1)."""

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
    """How many pairs of different random 8-letter words share a hash, for a given modulus."""
    r = random.Random(seed)
    words = {"".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(8)) for _ in range(n_strings)}
    seen, pairs = {}, 0
    for w in words:
        h = PrefixHash(w, mod=mod).get(0, len(w))
        pairs += seen.get(h, 0)
        seen[h] = seen.get(h, 0) + 1
    return pairs


def thue_morse(n: int) -> str:
    """The Thue-Morse word of length 2^n over a and b: start with a, and repeatedly append the swapped copy."""
    w = "a"
    for _ in range(n):
        w += w.translate(str.maketrans("ab", "ba"))
    return w


def whole_hash(s: str, base: int, mod: int) -> int:
    """The polynomial hash of a whole string, for any base and modulus (Section 34.6)."""
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % mod
    return h


def overflow_attack(n: int = 10, base: int = BASE) -> tuple[bool, bool]:
    """Anti-hash input (Section 34.6): the Thue-Morse word of length 2^n and its swapped copy. Returns (collide
    modulo 2^64, as with unchecked 64-bit overflow?, collide modulo the prime 2^61 - 1?)."""
    a = thue_morse(n)
    b = a.translate(str.maketrans("ab", "ba"))
    return whole_hash(a, base, 1 << 64) == whole_hash(b, base, 1 << 64), whole_hash(a, base, MOD) == whole_hash(b, base, MOD)


class DoubleHash:
    """Two independent prefix hashes with random bases (Section 34.6): a false match needs both to collide."""

    def __init__(self, s: str, seed: int | None = None):
        r = random.Random(seed)
        self.h1 = PrefixHash(s, base=r.randrange(256, MOD - 1), mod=MOD)
        self.h2 = PrefixHash(s, base=r.randrange(256, 1_000_000_006), mod=1_000_000_007)

    def get(self, a: int, b: int) -> tuple[int, int]:
        return self.h1.get(a, b), self.h2.get(a, b)


if __name__ == "__main__":
    s = "the club reads; the club meets"
    print(same(s, 0, 8, 16, 24), same(s, 4, 8, 20, 24), same(s, 0, 3, 4, 7))
    print(distinct_of_length("banana", 2), distinct_of_length("banana", 3), longest_repeat("banana"), repr(longest_repeat(s)))
    for mod in (1000, 100_000, 10_000_000, MOD):
        print(mod, collisions(10_000, mod))
