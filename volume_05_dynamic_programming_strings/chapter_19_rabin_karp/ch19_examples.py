"""Volume 5, Chapter 19 - Rabin-Karp: compare fingerprints first, letters only when fingerprints agree.

Run:  python3 ch19_examples.py
"""

from __future__ import annotations

import random

BASE = 256


def fingerprint(s: str, mod: int) -> int:
    h = 0
    for ch in s:
        h = (h * BASE + ord(ch)) % mod
    return h


def rabin_karp(text: str, pattern: str, mod: int = 1_000_000_007) -> tuple[list, int, int]:
    """Slide a rolling fingerprint along the text (Figure 19.2). Returns (positions, fingerprint matches checked
    letter by letter, false alarms)."""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1)), 0, 0
    if m > n:
        return [], 0, 0
    target, h = fingerprint(pattern, mod), fingerprint(text[:m], mod)
    top = pow(BASE, m - 1, mod)                       # weight of the letter leaving the window
    found, checked, false = [], 0, 0
    for s in range(n - m + 1):
        if h == target:
            checked += 1
            if text[s:s + m] == pattern:
                found.append(s)
            else:
                false += 1                            # same fingerprint, different letters
        if s + m < n:
            h = ((h - ord(text[s]) * top) * BASE + ord(text[s + m])) % mod   # roll: drop one letter, add the next
    return found, checked, false


def many_patterns(text: str, patterns: list, mod: int = 1_000_000_007) -> dict:
    """Several patterns of the same length at once: one fingerprint per window, looked up in a set."""
    m = len(patterns[0])
    want = {fingerprint(p, mod): p for p in patterns}
    hits = {p: [] for p in patterns}
    for s in range(len(text) - m + 1):
        w = text[s:s + m]
        if fingerprint(w, mod) in want and w in hits:
            hits[w].append(s)
    return hits


NEWSLETTER = "the reading club meets on monday; the club reads maps and poems at the library"

if __name__ == "__main__":
    print(rabin_karp(NEWSLETTER, "club"))
    print(rabin_karp(NEWSLETTER, "club", mod=7))
    r = random.Random(19)
    t = "".join(r.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(10000))
    for mod in (7, 101, 1_000_000_007):
        print(mod, rabin_karp(t, "library", mod))
    print(rabin_karp("a" * 1000, "a" * 9 + "b"))
    print(many_patterns(NEWSLETTER, ["club", "maps", "read"]))
