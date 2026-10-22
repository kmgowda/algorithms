"""Volume 5, Chapter 19 - Thinking Problems.

Problem 1: the rent-then-buy rule pays less than twice the best; when buy is a multiple of rent, at most 2 - rent/buy.
Problem 2: split a request list into phases of k different books; LRU misses at most k per phase,
           and any rule misses at least once per phase after the first.
Problem 3: "FIFO is never worse than LRU" is false: a short counterexample, found by search.
"""

from __future__ import annotations

import itertools

from ch19_examples import belady, fifo, lru, ski_best, ski_rental


def ratio_bound(rent: int, buy: int) -> float:
    return 2 - rent / buy


def phases(requests: list, k: int) -> int:
    """Greedy split: a phase is the longest stretch asking for at most k different books."""
    count, seen = 0, set()
    for b in requests:
        if b not in seen and len(seen) == k:
            count, seen = count + 1, set()
        seen.add(b)
    return count + (1 if seen else 0)


def lru_worse_than_fifo(k: int = 2, length: int = 7, alphabet: str = "ABC") -> list | None:
    """The shortest request list where LRU misses more than FIFO."""
    for n in range(1, length + 1):
        for seq in itertools.product(alphabet, repeat=n):
            if lru(list(seq), k) > fifo(list(seq), k):
                return list(seq)
    return None


def fifo_worse_than_lru(k: int = 2, length: int = 7, alphabet: str = "ABC") -> list | None:
    for n in range(1, length + 1):
        for seq in itertools.product(alphabet, repeat=n):
            if fifo(list(seq), k) > lru(list(seq), k):
                return list(seq)
    return None


if __name__ == "__main__":
    from ch19_examples import REQUESTS, SHELF
    print(ratio_bound(10, 100), phases(REQUESTS, SHELF), lru(REQUESTS, SHELF), belady(REQUESTS, SHELF))
    print(lru_worse_than_fifo(), fifo_worse_than_lru())
