"""Volume 2, Chapter 15 - model solution for Thinking Problem 2: a perfect table of words.

Run:  python3 ch15_solutions.py
"""

from __future__ import annotations

import random

from ch15_examples import PerfectTable, uh

Q = 1_000_003            # a prime larger than every number a word is turned into


def word_number(word: str, base: int) -> int:
    """Read the word as a number in the given base, mod Q (one pass over its letters)."""
    v = 0
    for ch in word:
        v = (v * base + ord(ch)) % Q
    return v


def locate(table: PerfectTable, x: int):
    """The (bucket, slot) where x would live in an FKS table, or None if its bucket is empty."""
    if table.m == 0:
        return None
    j = uh(table.a, table.b, table.p, table.m)(x)
    if table.buckets[j] is None:
        return None
    a, b, slots = table.buckets[j]
    return j, uh(a, b, table.p, len(slots))(x)


def build_word_table(words, seed: int = 1):
    """A static table of words with one full word comparison per lookup (Section 15.17).

    Draw a random base until the words turn into distinct numbers, then build an FKS table over the numbers.
    Returns a function contains(word).
    """
    words = list(dict.fromkeys(words))
    rng = random.Random(seed)
    while True:
        base = rng.randrange(256, Q)
        nums = [word_number(w, base) for w in words]
        if len(set(nums)) == len(nums):
            break                                      # no two words share a number: keep this base
    table = PerfectTable(nums, p=Q, seed=seed)
    stored = [None if bkt is None else [None] * len(bkt[2]) for bkt in table.buckets]
    for x, w in zip(nums, words):                      # the words, in the same places as their numbers
        j, i = locate(table, x)
        stored[j][i] = w

    def contains(word: str) -> bool:
        place = locate(table, word_number(word, base))
        return place is not None and stored[place[0]][place[1]] == word   # the one word comparison
    return contains


if __name__ == "__main__":
    has = build_word_table(["if", "else", "while", "for", "return", "def", "class", "and", "or"])
    print([has(w) for w in ("while", "whale", "or", "")])
