"""Volume 5, Chapter 23 - Suffix Arrays: sort every ending of a text once, then find any pattern by binary search.

Run:  python3 ch23_examples.py
"""

from __future__ import annotations

import bisect


def suffix_array_simple(text: str) -> list:
    """Sort the starting positions by the suffixes they begin (Figure 23.1): simple, about n^2 log n."""
    return sorted(range(len(text)), key=lambda i: text[i:])


def suffix_array_doubling(text: str) -> tuple[list, int]:
    """Prefix doubling (Figure 23.3): sort by the first 1, 2, 4, ... letters using ranks from the previous round.
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


def find_all(text: str, sa: list, pattern: str) -> tuple[list, int]:
    """Every occurrence: the suffixes starting with pattern form one block of the array, found by two binary
    searches (Figure 23.2). Returns (sorted positions, suffix comparisons)."""
    if not pattern:
        return list(range(len(text) + 1)), 0         # the same convention as Chapter 17
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
