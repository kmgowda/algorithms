"""Volume 13, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

from collections import Counter


def is_anagram(a: str, b: str) -> bool:
    """Exercise 1 (LeetCode 242): same letters, same counts."""
    return Counter(a) == Counter(b)


def reverse_complement(dna: str) -> str:
    """Exercise 2: the other DNA strand - reverse, then swap A<->T and C<->G."""
    return dna[::-1].translate(str.maketrans("ACGT", "TGCA"))


def most_common_word(text: str, banned: set[str]) -> str:
    """Exercise 3 (LeetCode 819): most frequent word ignoring case, punctuation and banned words."""
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    counts = Counter(w for w in cleaned.split() if w not in banned)
    return counts.most_common(1)[0][0]


if __name__ == "__main__":
    print(is_anagram("listen", "silent"), reverse_complement("ATGC"),
          most_common_word("Bob hit a ball, the hit BALL flew far after it was hit.", {"hit"}))
