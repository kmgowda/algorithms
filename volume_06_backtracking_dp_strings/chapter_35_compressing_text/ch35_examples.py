"""Volume 6, Chapter 35 - Compressing Text: run-length encoding and LZ77 (copy what came before).

Run:  python3 ch35_examples.py
"""

from __future__ import annotations

import random


def rle_encode(s: str, longest: int = 255) -> list:
    """Runs of the same letter as (letter, count) pairs (Figure 35.1). A count is stored in one byte, so a run
    longer than 255 is split into several pairs."""
    out = []
    for ch in s:
        if out and out[-1][0] == ch and out[-1][1] < longest:
            out[-1] = (ch, out[-1][1] + 1)
        else:
            out.append((ch, 1))
    return out


def rle_decode(runs: list) -> str:
    return "".join(ch * n for ch, n in runs)


def lz77_encode(s: str, window: int = 255, longest: int = 255) -> list:
    """Each step outputs (distance back, length to copy, next letter): the longest earlier match within the window,
    then one new letter (Figure 35.2). Matches may overlap the text being produced. Distance and length each fit in
    one byte."""
    out, i = [], 0
    while i < len(s):
        best_len, best_dist = 0, 0
        for j in range(max(0, i - window), i):
            k = 0
            while i + k < len(s) - 1 and k < longest and s[j + k] == s[i + k]:
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


def lzw_encode(s: str) -> tuple[list, dict]:
    """LZW (Section 35.6): a dictionary starts with every single letter that occurs; output the code of the longest
    word in the dictionary, then add that word plus the next letter as a new entry. Returns (codes, dictionary)."""
    letters = sorted(set(s))
    codes = {ch: i for i, ch in enumerate(letters)}
    out, w = [], ""
    for ch in s:
        if w + ch in codes:
            w += ch
        else:
            out.append(codes[w])
            codes[w + ch] = len(codes)
            w = ch
    if w:
        out.append(codes[w])
    return out, codes


def lzw_decode(codes: list, letters: list) -> str:
    """Rebuild the text and the same dictionary from the codes alone (plus the starting letters). The one tricky
    case: a code that is not in the dictionary yet must be the previous word plus its own first letter."""
    words = {i: ch for i, ch in enumerate(letters)}
    if not codes:
        return ""
    prev = words[codes[0]]
    out = [prev]
    for c in codes[1:]:
        cur = words[c] if c in words else prev + prev[0]          # the cScSc case
        out.append(cur)
        words[len(words)] = prev + cur[0]
        prev = cur
    return "".join(out)


def bwt(s: str, end: str = "$") -> tuple[str, list]:
    """Burrows-Wheeler transform (Section 35.7): sort every rotation of s + end, and keep the last letters.
    The sorted rotations are the suffix array of Chapter 31 in disguise. Returns (last column, sorted rotations)."""
    t = s + end
    rotations = sorted(t[i:] + t[:i] for i in range(len(t)))
    return "".join(r[-1] for r in rotations), rotations


def inverse_bwt(last: str, end: str = "$") -> str:
    """Undo the transform with the last-to-first mapping. Row r of the sorted rotations ends with last[r], the letter
    just before row r's first letter in the text. The k-th copy of a letter in the last column is the k-th copy of it
    in the first column (the sorted letters), so LF(r) = (where that letter starts in the first column) + k.
    Start from the row that begins with the end marker and walk backwards through the text."""
    if not last:
        return ""
    seen, rank = {}, []
    for ch in last:
        rank.append(seen.get(ch, 0))
        seen[ch] = seen.get(ch, 0) + 1
    start, total = {}, 0
    for ch in sorted(seen):
        start[ch] = total
        total += seen[ch]
    out, row = [], start[end]                          # the rotation that starts with the end marker
    for _ in range(len(last) - 1):
        out.append(last[row])                          # the letter before this rotation's start
        row = start[last[row]] + rank[row]             # last-to-first: the rotation starting with that letter
    return "".join(reversed(out))


def move_to_front(s: str) -> list:
    """Replace each letter by its position in a list that moves used letters to the front: runs become zeros."""
    table, out = sorted(set(s)), []
    for ch in s:
        i = table.index(ch)
        out.append(i)
        table.insert(0, table.pop(i))
    return out


def entropy_bits(s: str) -> float:
    """Shannon's limit (Section 35.8): the fewest bits per letter any code built from letter frequencies alone can
    average, sum of -p log2 p over the letters, times the length."""
    from math import log2
    n = len(s)
    if n == 0:
        return 0.0
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return -sum(c * log2(c / n) for c in counts.values())


POEM = "the club reads, the club meets, the club reads again"

if __name__ == "__main__":
    print(rle_encode("aaabccddddd"), sizes("aaabccddddd"))
    print(lz77_encode("abababab"), lz77_decode(lz77_encode("abababab")))
    print(sizes(POEM), lz77_encode(POEM)[-4:])
    r = random.Random(27)
    rnd = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(300))
    print(sizes(rnd), sizes("a" * 300), sizes("ab" * 150))
