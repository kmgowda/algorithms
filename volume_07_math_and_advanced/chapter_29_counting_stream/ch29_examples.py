"""Volume 7, Chapter 26 - Counting in a Stream: majority, frequent items, and distinct counts in tiny memory.

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


def majority_trace(stream) -> list:
    """(vote, candidate, counter) after each vote, for a hand trace."""
    cand, count, out = None, 0, []
    for x in stream:
        if count == 0:
            cand, count = x, 1
        else:
            count += 1 if x == cand else -1
        out.append((x, cand, count))
    return out


def space_saving(stream, k: int) -> dict:
    """Metwally, Agrawal and El Abbadi's Space-Saving (Figure 26.3): k counters; a new item takes over the smallest
    counter and adds 1 to it. Every count is an overestimate by at most n/k, and every item above n/k is kept."""
    counters = {}
    for x in stream:
        if x in counters:
            counters[x] += 1
        elif len(counters) < k:
            counters[x] = 1
        else:
            low = min(counters, key=lambda key: (counters[key], str(key)))
            counters[x] = counters.pop(low) + 1
    return counters


def h64(x, salt: str = "") -> int:
    return int(hashlib.sha256((salt + str(x)).encode()).hexdigest()[:16], 16)


def trailing_zeros(v: int, bits: int = 64) -> int:
    return bits if v == 0 else (v & -v).bit_length() - 1


def flajolet_martin(stream, copies: int = 64) -> float:
    """Flajolet and Martin (1985), Figure 26.5: for each hash value note its number of trailing zero bits r and mark
    bit r of a bitmap. A run of r zeros turns up about once in every 2^(r+1) distinct items, so the bitmap fills
    from the bottom; R = the position of its first unmarked bit is about log2(0.77351 n). Average R over many
    independent hashes: estimate 2^(average R) / 0.77351."""
    maps = [0] * copies
    for x in stream:
        for c in range(copies):
            maps[c] |= 1 << trailing_zeros(h64(x, str(c)))
    firsts = [trailing_zeros(~m & ((1 << 65) - 1)) for m in maps]
    return 2 ** (sum(firsts) / copies) / 0.77351


def hyperloglog(stream, b: int = 10) -> float:
    """HyperLogLog (Flajolet, Fusy, Gandouet and Meunier, 2007), Figure 26.6: the first b bits of a 64-bit hash choose
    one of m = 2^b registers; the register keeps the largest "rank" (position of the first 1 bit) of the remaining
    bits. Estimate alpha_m m^2 / sum of 2^(-register), with the small-range correction m ln(m / empty registers)."""
    import math
    m = 1 << b
    reg = [0] * m
    for x in stream:
        v = h64(x)
        j = v >> (64 - b)
        w = v & ((1 << (64 - b)) - 1)
        rank = (64 - b) - w.bit_length() + 1
        reg[j] = max(reg[j], rank)
    alpha = 0.7213 / (1 + 1.079 / m)
    est = alpha * m * m / sum(2.0 ** -r for r in reg)
    empty = reg.count(0)
    if est <= 2.5 * m and empty:
        est = m * math.log(m / empty)
    return est


if __name__ == "__main__":
    print(majority("ABAACAADA"), majority("ABCABC"), majority([]))
    r = random.Random(26)
    loans = [r.choice(["Dune"] * 30 + ["Emma"] * 20 + ["Hamlet"] * 12) if r.random() < 0.5 else f"book{r.randrange(5000)}" for _ in range(20000)]
    true = Counter(loans)
    print(true.most_common(3), misra_gries(loans, 10))
    visitors = [f"card{r.randrange(30000)}" for _ in range(100000)]
    print(len(set(visitors)), round(distinct_estimate(visitors, 64)), round(distinct_estimate(visitors, 1024)))
    print(majority_trace("ABAACAADA"))
    print(sorted(space_saving(loans, 9).items(), key=lambda t: -t[1])[:4])
    print(round(flajolet_martin(visitors, 64)), round(hyperloglog(visitors, 10)), round(hyperloglog(visitors, 6)))
    print(round(1.04 / 2 ** 5, 3), round(1.04 / 2 ** 3, 3), round(1 / (64 - 2) ** 0.5, 3), round(1 / (1024 - 2) ** 0.5, 3))
