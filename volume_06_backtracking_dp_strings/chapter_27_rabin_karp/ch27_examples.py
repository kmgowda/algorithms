"""Volume 6, Chapter 27 - Rabin-Karp: compare fingerprints first, letters only when fingerprints agree.

Run:  python3 ch27_examples.py
"""

from __future__ import annotations

import random

BASE = 256


def fingerprint(s: str, mod: int, base: int = BASE) -> int:
    """The window read as a number in the given base, kept as its remainder modulo mod (Section 27.4)."""
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % mod
    return h


def rabin_karp(text: str, pattern: str, mod: int = 1_000_000_007, base: int = BASE) -> tuple[list, int, int]:
    """Slide a rolling fingerprint along the text. Returns (positions, fingerprint matches checked
    letter by letter, false alarms)."""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1)), 0, 0
    if m > n:
        return [], 0, 0
    target, h = fingerprint(pattern, mod, base), fingerprint(text[:m], mod, base)
    top = pow(base, m - 1, mod)                       # weight of the letter leaving the window
    found, checked, false = [], 0, 0
    for s in range(n - m + 1):
        if h == target:
            checked += 1
            if text[s:s + m] == pattern:
                found.append(s)
            else:
                false += 1                            # same fingerprint, different letters
        if s + m < n:
            h = ((h - ord(text[s]) * top) * base + ord(text[s + m])) % mod   # roll: drop one letter, add the next
    return found, checked, false


def many_patterns(text: str, patterns: list, mod: int = 1_000_000_007) -> dict:
    """Several patterns of the same length at once: one rolling fingerprint per window, looked up in a set."""
    m, n = len(patterns[0]), len(text)
    want = {}
    for p in patterns:
        want.setdefault(fingerprint(p, mod), []).append(p)
    hits = {p: [] for p in patterns}
    if m > n:
        return hits
    h, top = fingerprint(text[:m], mod), pow(BASE, m - 1, mod)
    for s in range(n - m + 1):
        for p in want.get(h, ()):
            if text[s:s + m] == p:                     # check letters: fingerprints can collide
                hits[p].append(s)
        if s + m < n:
            h = ((h - ord(text[s]) * top) * BASE + ord(text[s + m])) % mod
    return hits


def random_text(n: int = 10000, seed: int = 30) -> str:
    """The shared random text of Part III (the same as Chapters 25, 29 and 38)."""
    r = random.Random(seed)
    return "".join(r.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(n))


def find_collision(m: int, mod: int, base: int = BASE, seed: int = 0) -> tuple[str, str]:
    """Two different m-letter words with the same fingerprint (Section 27.6): try random words until two share a
    fingerprint. With the base and modulus known, about the square root of mod tries are enough (the birthday
    effect, Chapter 34), which is how an attacker would fill a text with false alarms."""
    r, seen = random.Random(seed), {}
    while True:
        w = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(m))
        h = fingerprint(w, mod, base)
        if h in seen and seen[h] != w:
            return seen[h], w
        seen[h] = w


def colliding_bases(a: str, b: str, mod: int) -> int:
    """How many bases 0..mod-1 make two different same-length words collide: at most len(a) - 1, because the
    difference of their fingerprints is a polynomial in the base of degree < len(a), with at most that many roots."""
    return sum(1 for base in range(mod) if fingerprint(a, mod, base) == fingerprint(b, mod, base))


NEWSLETTER = "the reading club meets on monday; the club reads maps and poems at the library"

if __name__ == "__main__":
    print(rabin_karp(NEWSLETTER, "club"))
    print(rabin_karp(NEWSLETTER, "club", mod=7))
    t = random_text()
    for mod in (7, 101, 1_000_000_007):
        print(mod, rabin_karp(t, "library", mod))
    print(rabin_karp("a" * 1000, "a" * 9 + "b"))
    print(many_patterns(NEWSLETTER, ["club", "maps", "read"]))
