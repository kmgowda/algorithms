"""Volume 6, Chapter 26 - Counting in a Stream: majority, frequent items, and distinct counts in tiny memory.

Run:  python3 ch26_examples.py
"""

from __future__ import annotations

import hashlib
import random
from collections import Counter


def majority(stream) -> object | None:
    """Boyer-Moore vote (Figure 26.1): one candidate and one counter. Returns the majority item, or None if none exists
    (a second pass confirms)."""
    items = list(stream)
    cand, count = None, 0
    for x in items:
        if count == 0:
            cand, count = x, 1
        else:
            count += 1 if x == cand else -1
    return cand if items and items.count(cand) * 2 > len(items) else None


def misra_gries(stream, k: int) -> dict:
    """Keep at most k - 1 counters (Figure 26.2); every item seen more than n/k times survives."""
    counters = {}
    for x in stream:
        if x in counters:
            counters[x] += 1
        elif len(counters) < k - 1:
            counters[x] = 1
        else:
            for key in list(counters):
                counters[key] -= 1
                if counters[key] == 0:
                    del counters[key]
    return counters


def h01(x) -> float:
    return int(hashlib.sha256(str(x).encode()).hexdigest()[:15], 16) / 16 ** 15


def distinct_estimate(stream, k: int = 64) -> float:
    """K minimum values (Figure 26.3): keep the k smallest hash values; if the k-th smallest is v, about (k - 1)/v distinct."""
    smallest = set()
    for x in stream:
        h = h01(x)
        if len(smallest) < k:
            smallest.add(h)
        elif h < max(smallest) and h not in smallest:
            smallest.remove(max(smallest))
            smallest.add(h)
    if len(smallest) < k:
        return float(len(smallest))                   # fewer than k distinct: the count is exact
    return (k - 1) / max(smallest)


if __name__ == "__main__":
    print(majority("ABAACAADA"), majority("ABCABC"), majority([]))
    r = random.Random(26)
    loans = [r.choice(["Dune"] * 30 + ["Emma"] * 20 + ["Hamlet"] * 12) if r.random() < 0.5 else f"book{r.randrange(5000)}" for _ in range(20000)]
    true = Counter(loans)
    print(true.most_common(3), misra_gries(loans, 10))
    visitors = [f"card{r.randrange(30000)}" for _ in range(100000)]
    print(len(set(visitors)), round(distinct_estimate(visitors, 64)), round(distinct_estimate(visitors, 1024)))
