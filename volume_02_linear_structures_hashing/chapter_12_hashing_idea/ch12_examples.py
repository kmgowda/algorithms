"""Volume 2, Chapter 12 - The Coat-Check: The Idea of Hashing.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import random


def letter_sum_hash(key: str, m: int) -> int:
    """Add the character codes, then take the remainder mod m (Figure 12.2). Ignores letter order."""
    return sum(ord(c) for c in key) % m


def multiply_add_hash(key: str, m: int) -> int:
    """h = (h * 31 + code) mod m for each character in order (Section 12.5)."""
    h = 0
    for c in key:
        h = (h * 31 + ord(c)) % m
    return h


def spread(keys: list[str], m: int, fn) -> list[int]:
    """How many keys land in each of the m slots."""
    counts = [0] * m
    for k in keys:
        counts[fn(k, m)] += 1
    return counts


def duplicates_pairwise(returns: list[int]) -> tuple[set[int], int]:
    """Brute force: compare every pair. Returns (duplicates, comparisons)."""
    dups, comparisons = set(), 0
    for i in range(len(returns)):
        for j in range(i + 1, len(returns)):
            comparisons += 1
            if returns[i] == returns[j]:
                dups.add(returns[i])
    return dups, comparisons


def duplicates_hashed(returns: list[int]) -> tuple[set[int], int]:
    """Section 12.8: hash each call number into a set. Returns (duplicates, looks)."""
    seen, dups, looks = set(), set(), 0
    for b in returns:
        looks += 1
        if b in seen:
            dups.add(b)
        else:
            seen.add(b)
    return dups, looks


def birthday_shared(people: int, slots: int = 365, trials: int = 20_000, seed: int = 1) -> float:
    """Fraction of random trials in which two people share a slot (the birthday paradox)."""
    rng = random.Random(seed)
    hits = sum(len({rng.randrange(slots) for _ in range(people)}) < people for _ in range(trials))
    return hits / trials


if __name__ == "__main__":
    names = ["Maya", "Ravi", "Ana", "Ben", "Leo", "Zoe"]
    print({n: letter_sum_hash(n, 8) for n in names}, letter_sum_hash("MAYA", 8))
    print(letter_sum_hash("ART", 8) == letter_sum_hash("RAT", 8), multiply_add_hash("AB", 8), multiply_add_hash("BA", 8))
    rng = random.Random(3)
    words = ["".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(5)) for _ in range(4000)]
    print("letter sum :", spread(words, 16, letter_sum_hash))
    print("multiply 31:", spread(words, 16, multiply_add_hash))
    day = [rng.randint(1, 2000) for _ in range(500)]
    print(duplicates_pairwise(day)[1], duplicates_hashed(day)[1], duplicates_pairwise(day)[0] == duplicates_hashed(day)[0])
    print(round(birthday_shared(23), 3))
