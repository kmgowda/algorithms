"""Volume 5, Chapter 27 - Compressing Text: run-length encoding and LZ77 (copy what came before).

Run:  python3 ch27_examples.py
"""

from __future__ import annotations

import random


def rle_encode(s: str) -> list:
    """Runs of the same letter as (letter, count) pairs (Figure 27.1)."""
    out = []
    for ch in s:
        if out and out[-1][0] == ch:
            out[-1] = (ch, out[-1][1] + 1)
        else:
            out.append((ch, 1))
    return out


def rle_decode(runs: list) -> str:
    return "".join(ch * n for ch, n in runs)


def lz77_encode(s: str, window: int = 255) -> list:
    """Each step outputs (distance back, length to copy, next letter): the longest earlier match, then one new letter
    (Figure 27.2). Matches may overlap the text being produced."""
    out, i = [], 0
    while i < len(s):
        best_len, best_dist = 0, 0
        for j in range(max(0, i - window), i):
            k = 0
            while i + k < len(s) - 1 and s[j + k] == s[i + k]:
                k += 1
            if k > best_len:
                best_len, best_dist = k, i - j
        out.append((best_dist, best_len, s[i + best_len]))
        i += best_len + 1
    return out


def lz77_decode(triples: list) -> str:
    out = []
    for dist, length, ch in triples:
        start = len(out) - dist
        for k in range(length):
            out.append(out[start + k])                # copying one letter at a time allows overlapping copies
        out.append(ch)
    return "".join(out)


def sizes(s: str) -> tuple[int, int, int]:
    """Bytes: original, run-length (2 per run), LZ77 (3 per triple)."""
    return len(s), 2 * len(rle_encode(s)), 3 * len(lz77_encode(s))


POEM = "the club reads, the club meets, the club reads again"

if __name__ == "__main__":
    print(rle_encode("aaabccddddd"), sizes("aaabccddddd"))
    print(lz77_encode("abababab"), lz77_decode(lz77_encode("abababab")))
    print(sizes(POEM), lz77_encode(POEM)[-4:])
    r = random.Random(27)
    rnd = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(300))
    print(sizes(rnd), sizes("a" * 300), sizes("ab" * 150))
