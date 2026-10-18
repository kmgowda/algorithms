"""Volume 13, Chapter 2 - Naive String Matching.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import random


def naive_search(text: str, pattern: str) -> tuple[list[int], int]:
    """Try every starting position; compare left to right until a mismatch.
    Returns (occurrences, character comparisons made). Worst case O((n - m + 1) x m)."""
    n, m = len(text), len(pattern)
    found, comparisons = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            found.append(i)
    return found, comparisons


def first_occurrence(text: str, pattern: str) -> int:
    """LeetCode 28: index of the first occurrence, or -1 (an empty pattern is found at 0)."""
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i + len(pattern)] == pattern:
            return i
    return -1


def worst_case(n: int, m: int) -> tuple[str, str]:
    """The text 'aaaa...a' and pattern 'aa...ab': every alignment matches m - 1 letters before failing."""
    return "a" * n, "a" * (m - 1) + "b"


def random_case(n: int, m: int, alphabet: str, seed: int = 0) -> tuple[str, str]:
    rng = random.Random(seed)
    return "".join(rng.choice(alphabet) for _ in range(n)), "".join(rng.choice(alphabet) for _ in range(m))


def count_words(document: str, word: str) -> int:
    """Beginner example: how many times a word appears (whole words, case-insensitive)."""
    words = [w.strip(".,!?;:").lower() for w in document.split()]
    return sum(1 for w in words if w == word.lower())


def find_motif(genome: str, motif: str) -> list[int]:
    """Industry example: positions of a short DNA motif (e.g. a protein binding site) in a genome."""
    return naive_search(genome.upper(), motif.upper())[0]


if __name__ == "__main__":
    print(naive_search("abracadabra", "abra"))
    t, p = worst_case(10000, 50)
    print("worst case comparisons:", naive_search(t, p)[1], "for n = 10000, m = 50")
    t, p = random_case(10000, 50, "abcdefghijklmnopqrstuvwxyz")
    print("random English-like letters:", naive_search(t, p)[1])
    t, p = random_case(10000, 50, "ACGT")
    print("random DNA:", naive_search(t, p)[1])
    print(first_occurrence("sadbutsad", "sad"), count_words("The cat sat. The cat ran!", "cat"))
    print(find_motif("ttgacatttgacaTATAAT", "tgaca"))
