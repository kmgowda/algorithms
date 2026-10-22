"""Volume 6, Chapter 31 - Thinking Problems.

Problem 1: the suffixes that start with a pattern form one unbroken block of the suffix array (checked).
Problem 2: the longest beginning of a query that occurs in the text, by binary search on its length.
Problem 3: binary searching whole suffixes instead of their first m letters misses occurrences.
"""

from __future__ import annotations

import bisect

from ch31_examples import find_all


def longest_occurring_prefix(text: str, sa: list, query: str) -> str:
    lo, hi = 0, len(query)                             # query[:lo] occurs; query[:hi + 1] is unknown
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if find_all(text, sa, query[:mid])[0]:
            lo = mid
        else:
            hi = mid - 1
    return query[:lo]


def find_all_whole_suffixes(text: str, sa: list, pattern: str) -> list:
    suffixes = [text[i:] for i in sa]
    lo, hi = bisect.bisect_left(suffixes, pattern), bisect.bisect_right(suffixes, pattern)
    return sorted(sa[lo:hi])


if __name__ == "__main__":
    from ch31_examples import suffix_array_simple
    sa = suffix_array_simple("banana")
    print(longest_occurring_prefix("banana", sa, "nanny"), find_all_whole_suffixes("banana", sa, "ana"), find_all("banana", sa, "ana")[0])
