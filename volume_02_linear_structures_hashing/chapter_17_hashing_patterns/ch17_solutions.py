"""Volume 2, Chapter 17 - Thinking Problems.

Problem 2: count every pair of positions i < j whose prices sum to the card, in one pass with a map of counts.
Problem 3: the letter-sum anagram signature, kept here so the tests can show that it merges non-anagrams.
"""

from __future__ import annotations


def count_pairs_for_card(prices: list[int], card: int) -> int:
    seen: dict[int, int] = {}              # price -> how many times seen so far
    pairs = 0
    for p in prices:
        pairs += seen.get(card - p, 0)     # every earlier partner makes one pair
        seen[p] = seen.get(p, 0) + 1       # only after the check
    return pairs


def group_by_letter_sum(words: list[str]) -> dict[int, list[str]]:
    """WRONG as an anagram signature: different letters can have the same sum."""
    groups: dict[int, list[str]] = {}
    for w in words:
        groups.setdefault(sum(ord(c) for c in w), []).append(w)
    return groups


if __name__ == "__main__":
    print(count_pairs_for_card([15, 12, 15, 18, 15], 30), group_by_letter_sum(["cat", "act", "gap"]))
