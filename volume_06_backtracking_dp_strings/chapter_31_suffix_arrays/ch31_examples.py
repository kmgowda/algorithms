"""Volume 6, Chapter 31 - Suffix Arrays: sort every ending of a text once, then find any pattern by binary search.

Run:  python3 ch31_examples.py
"""

from __future__ import annotations

import bisect


def suffix_array_simple(text: str) -> list:
    """Sort the starting positions by the suffixes they begin: simple, about n^2 log n."""
    return sorted(range(len(text)), key=lambda i: text[i:])


def suffix_array_doubling(text: str) -> tuple[list, int]:
    """Prefix doubling (Figure 31.1): sort by the first 1, 2, 4, ... letters using ranks from the previous round.
    Returns (suffix array, rounds)."""
    n = len(text)
    if n == 0:
        return [], 0
    rank = [ord(c) for c in text]
    sa, k, rounds = list(range(n)), 1, 0
    while True:
        rounds += 1
        key = lambda i: (rank[i], rank[i + k] if i + k < n else -1)
        sa.sort(key=key)
        new = [0] * n
        for a, b in zip(sa, sa[1:]):
            new[b] = new[a] + (key(a) != key(b))
        rank = new
        if rank[sa[-1]] == n - 1 or k >= n:
            return sa, rounds
        k *= 2


def doubling_trace(text: str) -> list:
    """Prefix doubling round by round (Figure 31.1). Each entry is (k, the pair (rank[i], rank[i + k]) for every
    position i, the new ranks), starting from ranks of single letters (a = 0, b = 1, ...); -1 means "past the end"."""
    n = len(text)
    letters = sorted(set(text))
    rank = [letters.index(c) for c in text]
    out, k = [(0, None, list(rank))], 1
    while n and (len(set(rank)) < n):
        pairs = [(rank[i], rank[i + k] if i + k < n else -1) for i in range(n)]
        order = sorted(set(pairs))
        rank = [order.index(p) for p in pairs]
        out.append((k, pairs, list(rank)))
        k *= 2
    return out


def counting_sort(items: list, key, size: int) -> list:
    """A stable sort of items by an integer key from -1 to size - 1 (Volume 4's counting sort)."""
    buckets = [[] for _ in range(size + 1)]
    for it in items:
        buckets[key(it) + 1].append(it)
    return [it for b in buckets for it in b]


def suffix_array_radix(text: str) -> tuple[list, int]:
    """Prefix doubling with radix sorting (Section 31.5): each round sorts the pairs with two stable counting-sort
    passes, by second rank and then by first rank, so a round costs O(n) and the whole build O(n log n).
    Returns (suffix array, rounds)."""
    n = len(text)
    if n == 0:
        return [], 0
    letters = sorted(set(text))
    rank = [letters.index(c) for c in text]
    if len(set(rank)) == n:                            # all letters different: one sort by letter is enough
        return sorted(range(n), key=lambda i: rank[i]), 0
    sa, k, rounds = list(range(n)), 1, 0
    while True:
        rounds += 1
        second = lambda i: rank[i + k] if i + k < n else -1
        sa = counting_sort(list(range(n)), second, n)            # pass 1: by the second key
        sa = counting_sort(sa, lambda i: rank[i], n)             # pass 2: by the first key, keeping pass 1's order
        new = [0] * n
        for a, b in zip(sa, sa[1:]):
            new[b] = new[a] + ((rank[a], second(a)) != (rank[b], second(b)))
        rank = new
        k *= 2
        if len(set(rank)) == n:
            break
    return sa, rounds


def find_all(text: str, sa: list, pattern: str) -> tuple[list, int]:
    """Every occurrence: the suffixes starting with pattern form one block of the array, found by two binary
    searches. Returns (sorted positions, suffix comparisons)."""
    if not pattern:
        return list(range(len(text) + 1)), 0         # the same convention as Chapter 25
    comparisons = [0]
    m = len(pattern)

    class Prefixes:
        def __len__(self):
            return len(sa)

        def __getitem__(self, idx):
            comparisons[0] += 1
            return text[sa[idx]:sa[idx] + m]

    p = Prefixes()
    lo = bisect.bisect_left(p, pattern)
    hi = bisect.bisect_right(p, pattern)
    return sorted(sa[lo:hi]), comparisons[0]


if __name__ == "__main__":
    t = "banana"
    sa = suffix_array_simple(t)
    print(sa, [t[i:] for i in sa], suffix_array_doubling(t))
    print(find_all(t, sa, "ana"), find_all(t, sa, "nab"), find_all(t, sa, "a"))
    nl = "the reading club meets on monday; the club reads maps and poems at the library"
    sa2 = suffix_array_doubling(nl)[0]
    print(find_all(nl, sa2, "club"), find_all(nl, sa2, "the"), suffix_array_doubling(nl)[1])
