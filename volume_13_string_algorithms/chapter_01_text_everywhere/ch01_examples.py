"""Volume 13, Chapter 1 - Text Is Everywhere: Search Bars, DNA, Plagiarism.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import timeit
from collections import Counter


def code_points(text: str) -> list[int]:
    """Every character is stored as a number (its Unicode code point)."""
    return [ord(ch) for ch in text]


def utf8_bytes(text: str) -> int:
    """Bytes needed to store the text as UTF-8: 1 for English letters, 2-4 for other scripts and emoji."""
    return len(text.encode("utf-8"))


def build_with_plus(n: int) -> str:
    """Joining pieces one by one with + can copy the growing string each time (Python often optimises this)."""
    s = ""
    for i in range(n):
        s = s + str(i % 10)
    return s


def build_with_join(n: int) -> str:
    """Collect pieces in a list, join once: O(total length)."""
    return "".join(str(i % 10) for i in range(n))


def find_all_builtin(text: str, pattern: str) -> list[int]:
    """Python's own search (str.find), repeated to list every occurrence (overlaps allowed)."""
    out, i = [], text.find(pattern)
    while i != -1:
        out.append(i)
        i = text.find(pattern, i + 1)
    return out


def gc_content(dna: str) -> float:
    """Practical example: share of G and C bases in a DNA string - biologists use it to characterise genes."""
    counts = Counter(dna.upper())
    return (counts["G"] + counts["C"]) / max(1, len(dna))


def shingles(text: str, k: int) -> set[str]:
    """Industry example (plagiarism checks): the set of all k-word windows of a text."""
    words = text.lower().split()
    return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}


def similarity(a: str, b: str, k: int = 3) -> float:
    """Jaccard similarity of shingle sets: |A and B| / |A or B|."""
    sa, sb = shingles(a, k), shingles(b, k)
    return len(sa & sb) / len(sa | sb) if sa | sb else 1.0


if __name__ == "__main__":
    print(code_points("Hi!"), utf8_bytes("hello"), utf8_bytes("नमस्ते"), utf8_bytes("🙂"))
    t_plus = min(timeit.repeat(lambda: build_with_plus(20000), number=1, repeat=3))
    t_join = min(timeit.repeat(lambda: build_with_join(20000), number=1, repeat=3))
    print(f"build 20000 chars: + {t_plus * 1000:.2f} ms, join {t_join * 1000:.2f} ms")
    print("occurrences of 'ana':", find_all_builtin("bananarama banana", "ana"))
    print("GC content:", round(gc_content("ATGCGCATTA"), 2))
    essay = "the quick brown fox jumps over the lazy dog near the river bank"
    copied = "the quick brown fox jumps over the sleepy dog near the river bank"
    print("similarity:", round(similarity(essay, copied), 2))
