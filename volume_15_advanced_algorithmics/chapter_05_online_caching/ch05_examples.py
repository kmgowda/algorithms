"""Volume 15, Chapter 5 - Online Algorithms and Caching: Paging, Ski Rental.

An ONLINE algorithm must decide as each request arrives, without seeing the future. We compare it with the
best OFFLINE choice (which knows everything) - the 'competitive ratio'.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import random
from collections import OrderedDict, deque


def lru_misses(requests: list[str], size: int) -> int:
    """Least Recently Used: on a miss with a full cache, evict the page unused for the longest time."""
    cache: OrderedDict[str, None] = OrderedDict()
    misses = 0
    for page in requests:
        if page in cache:
            cache.move_to_end(page)
            continue
        misses += 1
        if len(cache) == size:
            cache.popitem(last=False)
        cache[page] = None
    return misses


def fifo_misses(requests: list[str], size: int) -> int:
    """First In, First Out: evict the page that entered earliest (ignores how recently it was used)."""
    cache: set[str] = set()
    order: deque[str] = deque()
    misses = 0
    for page in requests:
        if page in cache:
            continue
        misses += 1
        if len(cache) == size:
            cache.discard(order.popleft())
        cache.add(page)
        order.append(page)
    return misses


def belady_misses(requests: list[str], size: int) -> int:
    """OFFLINE optimum (Belady): evict the page whose next use is FARTHEST in the future. Needs the future,
    so it's a yardstick, not something a real cache can run."""
    cache: set[str] = set()
    misses = 0
    for i, page in enumerate(requests):
        if page in cache:
            continue
        misses += 1
        if len(cache) == size:
            def next_use(p: str) -> int:
                for j in range(i + 1, len(requests)):
                    if requests[j] == p:
                        return j
                return len(requests)
            cache.discard(max(cache, key=next_use))
        cache.add(page)
    return misses


def ski_rental(rent: int, buy: int, days_skied: int) -> tuple[int, int]:
    """Rent while the total rent stays below the purchase price, then buy (the 'break-even' rule).
    Returns (online cost, offline optimum). The online cost is always less than 2 x optimum."""
    rent_days = -(-buy // rent) - 1                  # rent this many days before buying
    online = days_skied * rent if days_skied <= rent_days else rent_days * rent + buy
    return online, min(days_skied * rent, buy)


def zipf_requests(n: int, pages: int, rng: random.Random) -> list[str]:
    """Realistic traffic: a few pages are very popular (probability proportional to 1 / rank)."""
    weights = [1 / r for r in range(1, pages + 1)]
    return [f"p{rng.choices(range(pages), weights)[0]}" for _ in range(n)]


def cache_report(requests: list[str], size: int) -> dict[str, int]:
    """Industry example: compare eviction policies on a request log before deploying a cache."""
    return {"LRU": lru_misses(requests, size), "FIFO": fifo_misses(requests, size), "optimal": belady_misses(requests, size)}


if __name__ == "__main__":
    reqs = list("ABCABDADBCDA")
    print("misses with 3 slots:", cache_report(reqs, 3))
    cycle = list("ABCD") * 5
    print("cycle of 4 pages in 3 slots:", cache_report(cycle, 3))
    print("Zipf traffic:", cache_report(zipf_requests(3000, 100, random.Random(1)), 10))
    for days in (3, 9, 10, 30):
        print(f"ski {days} days:", ski_rental(100, 1000, days))
