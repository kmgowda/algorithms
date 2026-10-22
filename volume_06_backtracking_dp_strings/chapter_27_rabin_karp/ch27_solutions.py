"""Volume 6, Chapter 27 - Thinking Problems.

Problem 1: the rolling update gives exactly the fingerprint of the next window (checked on every window).
Problem 2: how many different m-letter windows a text has, with rolling fingerprints and a letter check on ties.
Problem 3: trusting the fingerprint without checking letters reports false matches when the modulus is small.
"""

from __future__ import annotations

from ch27_examples import BASE, fingerprint


def rolled(text: str, m: int, mod: int, base: int = BASE) -> list:
    h, top, out = fingerprint(text[:m], mod, base), pow(base, m - 1, mod), []
    for s in range(len(text) - m + 1):
        out.append(h)
        if s + m < len(text):
            h = ((h - ord(text[s]) * top) * base + ord(text[s + m])) % mod
    return out


def distinct_windows(text: str, m: int, mod: int = 1_000_003) -> int:
    if m <= 0 or m > len(text):
        return 0 if m > len(text) else 1
    groups: dict = {}
    for s, h in enumerate(rolled(text, m, mod)):
        words = groups.setdefault(h, set())
        words.add(text[s:s + m])                      # the letter check: equal fingerprints may differ
    return sum(len(w) for w in groups.values())


def trusting_search(text: str, pattern: str, mod: int) -> list:
    target, m = fingerprint(pattern, mod), len(pattern)
    return [s for s, h in enumerate(rolled(text, m, mod)) if h == target]


if __name__ == "__main__":
    from ch27_examples import NEWSLETTER, rabin_karp
    print(distinct_windows(NEWSLETTER, 4), len({NEWSLETTER[i:i + 4] for i in range(len(NEWSLETTER) - 3)}))
    for mod in (7, 13, 101):
        print(mod, trusting_search(NEWSLETTER, "club", mod), rabin_karp(NEWSLETTER, "club", mod)[0])
