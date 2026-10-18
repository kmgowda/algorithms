"""Volume 6, Chapter 13 - Solutions to the exercises."""

from __future__ import annotations

import math


def disk_reads(n: int, structure: str) -> int:
    """Exercise 1: worst-case node visits (each could be a disk read) to find one key among n."""
    if structure == "AVL":
        return math.floor(1.44 * math.log2(n + 2))
    if structure == "red-black":
        return math.floor(2 * math.log2(n + 1))
    if structure == "B-tree t=500":
        return math.floor(math.log((n + 1) / 2, 500)) + 1
    raise ValueError(structure)


def pick_for(scenario: str) -> str:
    """Exercise 2: match real scenarios to structures."""
    return {
        "username lookup at login": "hash table",
        "leaderboard with 'who is just above me'": "balanced BST",
        "bank database index on account number": "B+ tree",
        "search-box suggestions": "trie",
        "a dictionary loaded once and never changed": "sorted array",
    }[scenario]


if __name__ == "__main__":
    print({s: disk_reads(10**9, s) for s in ("AVL", "red-black", "B-tree t=500")})
    print(pick_for("search-box suggestions"))
