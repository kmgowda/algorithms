"""Volume 7, Chapter 19 - Sampling a Stream: keep k fair picks from a stream of unknown length (reservoir sampling).

Run:  python3 ch19_examples.py
"""

from __future__ import annotations

import random
from collections import Counter


def reservoir(stream, k: int, rng) -> list:
    """Keep the first k; item number i (from 1) replaces a random kept item with probability k / i (Figure 19.2)."""
    if k < 0:
        raise ValueError("k must be 0 or more")
    kept = []
    for i, item in enumerate(stream, start=1):
        if i <= k:
            kept.append(item)
        else:
            j = rng.randrange(i)
            if j < k:
                kept[j] = item
    return kept


def weighted_pick(items: list, weights: list, rng):
    """One pick, chance proportional to weight, in one pass (a reservoir with weights)."""
    total, chosen = 0, None
    for item, w in zip(items, weights):
        if w < 0:
            raise ValueError("weights must not be negative")
        total += w
        if w and rng.random() * total < w:
            chosen = item
    return chosen


def exact_inclusion(n: int, k: int) -> list:
    """Run reservoir sampling on every possible sequence of random choices (each equally likely) and return, for each
    item, the exact fraction of runs that end with it in the sample (Figure 19.3)."""
    import itertools
    from fractions import Fraction
    choice_ranges = [range(i) for i in range(k + 1, n + 1)]
    counts, runs = [0] * n, 0

    class Feed:
        def __init__(self, cs):
            self.cs = iter(cs)

        def randrange(self, m):
            return next(self.cs)

    for cs in itertools.product(*choice_ranges):
        runs += 1
        for x in reservoir(range(n), k, Feed(cs)):
            counts[x] += 1
    return [Fraction(c, runs) for c in counts]


def weighted_sample(items: list, weights: list, k: int, rng) -> list:
    """k picks without repetition, each step proportional to weight, in one pass (Efraimidis and Spirakis):
    give each item the key u^(1/w) with u uniform in (0, 1), and keep the k largest keys with a heap."""
    import heapq
    heap = []
    for item, w in zip(items, weights):
        if w < 0:
            raise ValueError("weights must not be negative")
        if w == 0:
            continue
        key = rng.random() ** (1 / w)
        if len(heap) < k:
            heapq.heappush(heap, (key, item))
        elif k and key > heap[0][0]:
            heapq.heapreplace(heap, (key, item))
    return [item for _, item in sorted(heap, reverse=True)]


def reservoir_skipping(stream, k: int, rng) -> tuple[list, int]:
    """Li's Algorithm L: instead of one random number per item, jump straight to the next item that will enter,
    using about k (1 + ln(n / k)) random numbers. Returns (sample, random numbers used)."""
    import math
    it = iter(stream)
    kept, used = [], 0
    for _ in range(k):
        try:
            kept.append(next(it))
        except StopIteration:
            return kept, used
    if k == 0:
        return kept, used
    w = math.exp(math.log(rng.random()) / k)
    used += 1
    while True:
        skip = math.floor(math.log(rng.random()) / math.log(1 - w))
        used += 1
        try:
            for _ in range(skip):
                next(it)
            item = next(it)
        except StopIteration:
            return kept, used
        kept[rng.randrange(k)] = item
        w *= math.exp(math.log(rng.random()) / k)
        used += 2


def merge_reservoirs(sample1: list, n1: int, sample2: list, n2: int, k: int, rng) -> list:
    """Merge two reservoirs of size k kept over streams of n1 and n2 items into a fair sample of k from all n1 + n2.
    Fill each place from side 1 with chance r1 / (r1 + r2), where r1, r2 are the items of each stream not yet
    represented, and lower the chosen side's count by one (a hypergeometric draw)."""
    pool1, pool2 = list(sample1), list(sample2)
    r1, r2 = n1, n2
    out = []
    for _ in range(min(k, n1 + n2)):
        if rng.random() * (r1 + r2) < r1:
            out.append(pool1.pop(rng.randrange(len(pool1))))
            r1 -= 1
        else:
            out.append(pool2.pop(rng.randrange(len(pool2))))
            r2 -= 1
    return out


def merge_count_distribution(n1: int, n2: int, k: int, biased: bool = False) -> list:
    """Exact chance that the merge takes j items from side 1, j = 0..k. biased=True uses the fixed chance n1/(n1+n2)
    at every place (the wrong method); otherwise the counts go down as places fill (the right one)."""
    from fractions import Fraction
    dist = {(0, n1, n2): Fraction(1)}
    for _ in range(k):
        new = {}
        for (j, r1, r2), pr in dist.items():
            p1 = Fraction(n1, n1 + n2) if biased else Fraction(r1, r1 + r2)
            for (dj, nr1, nr2, q) in ((1, r1 - 1, r2, p1), (0, r1, r2 - 1, 1 - p1)):
                if q:
                    key = (j + dj, nr1, nr2)
                    new[key] = new.get(key, 0) + pr * q
        dist = new
    out = [Fraction(0)] * (k + 1)
    for (j, _, _), pr in dist.items():
        out[j] += pr
    return out


if __name__ == "__main__":
    rng = random.Random(19)
    counts = Counter()
    for _ in range(30000):
        counts.update(reservoir(range(10), 3, rng))
    print(sorted(counts.items()))
    print(reservoir(range(2), 5, rng), reservoir([], 3, rng), reservoir(range(100), 0, rng))
    w = Counter(weighted_pick(["a", "b", "c"], [1, 2, 7], rng) for _ in range(10000))
    print(sorted(w.items()))
    print(exact_inclusion(5, 2))
    ws = Counter()
    for _ in range(20000):
        ws.update(weighted_sample(["a", "b", "c", "d"], [1, 2, 3, 4], 2, rng))
    print(sorted(ws.items()))
    print(reservoir_skipping(range(1_000_000), 100, random.Random(5))[1], round(100 * (1 + __import__("math").log(10000))))
    print(merge_count_distribution(2, 2, 2), merge_count_distribution(2, 2, 2, biased=True))
    import math
    print([math.comb(2, j) * math.comb(2, 2 - j) for j in range(3)], math.comb(4, 2))
