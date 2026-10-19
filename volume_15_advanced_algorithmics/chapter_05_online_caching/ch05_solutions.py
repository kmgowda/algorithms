"""Volume 15, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

from collections import Counter


def lfu_misses(requests: list[str], size: int) -> int:
    """Exercise 1: Least Frequently Used - evict the cached page requested the fewest times so far
    (ties: the one that entered earliest)."""
    cache: dict[str, int] = {}
    counts: Counter[str] = Counter()
    misses = 0
    for t, page in enumerate(requests):
        counts[page] += 1
        if page in cache:
            continue
        misses += 1
        if len(cache) == size:
            victim = min(cache, key=lambda p: (counts[p], cache[p]))
            del cache[victim]
        cache[page] = t
    return misses


def worst_case_ratio(rent: int, buy: int, max_days: int) -> float:
    """Exercise 2: the worst online / optimal ratio of the break-even rule over all season lengths."""
    rent_days = -(-buy // rent) - 1
    worst = 1.0
    for days in range(1, max_days + 1):
        online = days * rent if days <= rent_days else rent_days * rent + buy
        worst = max(worst, online / min(days * rent, buy))
    return worst


def adversary_for_lru(size: int, length: int) -> list[str]:
    """Exercise 3: requests that make LRU miss every time - cycle through size + 1 pages."""
    return [f"p{i % (size + 1)}" for i in range(length)]


if __name__ == "__main__":
    print(lfu_misses(list("ABCABDADBCDA"), 3), round(worst_case_ratio(100, 1000, 100), 2), adversary_for_lru(2, 6))
