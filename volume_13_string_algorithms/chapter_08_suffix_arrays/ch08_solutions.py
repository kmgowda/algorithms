"""Volume 13, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from ch08_examples import lcp_array, suffix_array


def count_distinct_substrings(s: str) -> int:
    """Exercise 1: each suffix adds (its length - lcp with the previous suffix) new substrings."""
    sa = suffix_array(s)
    lcp = lcp_array(s, sa)
    return sum(len(s) - i for i in sa) - sum(lcp)


def longest_common_substring(a: str, b: str) -> str:
    """Exercise 2: join a + '\\x01' + b; the best LCP between neighbours from DIFFERENT strings is the answer."""
    s = a + "\x01" + b
    sa = suffix_array(s)
    lcp = lcp_array(s, sa)
    best_len, best_at = 0, 0
    for i, h in enumerate(lcp):
        if (sa[i] < len(a)) != (sa[i + 1] < len(a)) and h > best_len:
            best_len, best_at = h, sa[i]
    return s[best_at:best_at + best_len]


def kth_suffix(s: str, k: int) -> str:
    """Exercise 3: the k-th smallest suffix (1-based) - read it off the suffix array."""
    return s[suffix_array(s)[k - 1]:]


if __name__ == "__main__":
    print(count_distinct_substrings("banana"), longest_common_substring("xabxac", "abcabxabcd"), kth_suffix("banana", 2))
