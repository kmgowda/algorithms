"""Volume 13, Chapter 3 - Rabin-Karp: Rolling Hashes.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

BASE = 256
MOD = 1_000_000_007


def poly_hash(s: str, base: int = BASE, mod: int = MOD) -> int:
    """Treat the string as a number in base `base`, reduced modulo `mod` (Horner's rule, V10-C10)."""
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % mod
    return h


def rabin_karp(text: str, pattern: str, base: int = BASE, mod: int = MOD) -> tuple[list[int], int]:
    """Slide a window: update its hash in O(1) by removing the left letter and adding the right one.
    Only when hashes match do we compare letters (to rule out a collision).
    Returns (occurrences, spurious hits = equal hashes that were not real matches)."""
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return ([0] if m == 0 else []), 0
    high = pow(base, m - 1, mod)                  # weight of the window's first letter
    target, window = poly_hash(pattern, base, mod), poly_hash(text[:m], base, mod)
    found, spurious = [], 0
    for i in range(n - m + 1):
        if window == target:
            if text[i:i + m] == pattern:
                found.append(i)
            else:
                spurious += 1
        if i + m < n:
            window = ((window - ord(text[i]) * high) * base + ord(text[i + m])) % mod
    return found, spurious


def multi_pattern(text: str, patterns: list[str]) -> dict[str, list[int]]:
    """Many patterns of the SAME length: hash the text windows once and look each hash up in a dictionary."""
    m = len(patterns[0])
    assert all(len(p) == m for p in patterns)
    by_hash: dict[int, list[str]] = {}
    for p in patterns:
        by_hash.setdefault(poly_hash(p), []).append(p)
    out: dict[str, list[int]] = {p: [] for p in patterns}
    if len(text) < m:
        return out
    high = pow(BASE, m - 1, MOD)
    window = poly_hash(text[:m])
    for i in range(len(text) - m + 1):
        for p in by_hash.get(window, []):
            if text[i:i + m] == p:
                out[p].append(i)
        if i + m < len(text):
            window = ((window - ord(text[i]) * high) * BASE + ord(text[i + m])) % MOD
    return out


def shared_passages(a: str, b: str, length: int) -> set[str]:
    """Industry example (plagiarism): every `length`-character passage appearing in both documents."""
    def windows(s: str) -> dict[int, set[str]]:
        out: dict[int, set[str]] = {}
        if len(s) < length:
            return out
        high = pow(BASE, length - 1, MOD)
        h = poly_hash(s[:length])
        for i in range(len(s) - length + 1):
            out.setdefault(h, set()).add(s[i:i + length])
            if i + length < len(s):
                h = ((h - ord(s[i]) * high) * BASE + ord(s[i + length])) % MOD
        return out
    wa, wb = windows(a), windows(b)
    return {x for h in wa.keys() & wb.keys() for x in wa[h] & wb[h]}


if __name__ == "__main__":
    print(poly_hash("abc"), rabin_karp("abracadabra", "abra"))
    found, spurious = rabin_karp("abracadabra" * 50, "cad", mod=31)
    print("tiny modulus 31:", len(found), "matches,", spurious, "spurious hash hits")
    print(multi_pattern("the cat sat on the mat", ["cat", "mat", "dog"]))
    print(sorted(shared_passages("to be or not to be", "not to be outdone", 8)))
