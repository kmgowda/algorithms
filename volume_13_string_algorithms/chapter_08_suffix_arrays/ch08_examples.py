"""Volume 13, Chapter 8 - Suffix Arrays and Longest Common Prefix.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations


def suffix_array_simple(s: str) -> list[int]:
    """Sort the starting positions by the suffixes themselves: easy, O(n^2 log n) because comparisons copy strings."""
    return sorted(range(len(s)), key=lambda i: s[i:])


def suffix_array(s: str) -> list[int]:
    """Prefix doubling: sort by the first 1, 2, 4, 8 ... letters, using the ranks from the previous round.
    O(n log^2 n) with Python's sort."""
    n = len(s)
    rank = [ord(c) for c in s]
    sa = list(range(n))
    k = 1
    while True:
        key = [(rank[i], rank[i + k] if i + k < n else -1) for i in range(n)]
        sa.sort(key=lambda i: key[i])
        new = [0] * n
        for a, b in zip(sa, sa[1:]):
            new[b] = new[a] + (key[a] != key[b])
        rank = new
        if n == 0 or rank[sa[-1]] == n - 1:
            return sa                                 # all ranks distinct: fully sorted
        k *= 2


def lcp_array(s: str, sa: list[int]) -> list[int]:
    """Kasai's algorithm: lcp[i] = common prefix length of the suffixes at sa[i] and sa[i + 1]. O(n):
    moving from suffix i to i + 1 loses at most one letter of the previous answer."""
    n = len(s)
    rank = [0] * n
    for pos, i in enumerate(sa):
        rank[i] = pos
    lcp, h = [0] * max(0, n - 1), 0
    for i in range(n):
        if rank[i] == n - 1:
            h = 0
            continue
        j = sa[rank[i] + 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[rank[i]] = h
        if h:
            h -= 1
    return lcp


def find_all(s: str, sa: list[int], pattern: str) -> list[int]:
    """All occurrences by binary search: suffixes starting with the pattern form one block of the suffix array.
    O(m log n) per query - the text is indexed once, then queries are fast."""
    m = len(pattern)
    lo, hi = 0, len(sa)
    while lo < hi:                                    # first suffix whose start is >= pattern
        mid = (lo + hi) // 2
        if s[sa[mid]:sa[mid] + m] < pattern:
            lo = mid + 1
        else:
            hi = mid
    start, hi = lo, len(sa)
    while lo < hi:                                    # first suffix whose start is > pattern
        mid = (lo + hi) // 2
        if s[sa[mid]:sa[mid] + m] <= pattern:
            lo = mid + 1
        else:
            hi = mid
    return sorted(sa[start:lo])


def longest_repeated_substring(s: str) -> str:
    """The largest LCP between neighbouring suffixes is the longest substring occurring twice."""
    if len(s) < 2:
        return ""
    sa = suffix_array(s)
    lcp = lcp_array(s, sa)
    best = max(range(len(lcp)), key=lambda i: lcp[i])
    return s[sa[best]:sa[best] + lcp[best]]


def genome_index_queries(genome: str, probes: list[str]) -> dict[str, int]:
    """Industry example: index a genome once, then count many probe sequences quickly."""
    sa = suffix_array(genome)
    return {p: len(find_all(genome, sa, p)) for p in probes}


if __name__ == "__main__":
    s = "banana"
    sa = suffix_array(s)
    print(sa, [s[i:] for i in sa], lcp_array(s, sa))
    print(find_all(s, sa, "ana"), longest_repeated_substring("mississippi"))
    print(genome_index_queries("ACGTACGTTACGACG", ["ACG", "TAC", "GGG"]))
