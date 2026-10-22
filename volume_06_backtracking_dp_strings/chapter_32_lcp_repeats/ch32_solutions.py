"""Volume 6, Chapter 32 - Thinking Problems.

Problem 1: Kasai's h never drops by more than one between steps, so the method makes O(n) letter comparisons (checked).
Problem 2: the longest substring that occurs at least k times: the best minimum over k - 1 neighbouring LCP values.
Problem 3: forgetting to check that neighbours come from different strings returns a repeat inside one string.
"""

from __future__ import annotations

from ch32_examples import lcp_kasai, suffix_array


def kasai_comparisons(text: str) -> int:
    sa = suffix_array(text)
    n, rank, h, count = len(text), [0] * len(text), 0, 0
    for r, i in enumerate(sa):
        rank[i] = r
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n:
                count += 1
                if text[i + h] != text[j + h]:
                    break
                h += 1
            if h:
                h -= 1
        else:
            h = 0
    return count


def longest_repeat_k(text: str, k: int) -> str:
    if k <= 1:
        return text
    sa = suffix_array(text)
    lcp = lcp_kasai(text, sa)
    best, at = 0, 0
    for r in range(1, len(sa) - k + 2):
        m = min(lcp[r:r + k - 1])                      # shared by the k suffixes in rows r - 1 ... r + k - 2
        if m > best:
            best, at = m, sa[r]
    return text[at:at + best]


def longest_common_unchecked(a: str, b: str, sep: str = "\x01") -> str:
    t = a + sep + b
    sa = suffix_array(t)
    lcp = lcp_kasai(t, sa)
    r = max(range(len(lcp)), key=lambda k: lcp[k])
    return t[sa[r]:sa[r] + lcp[r]]


if __name__ == "__main__":
    from ch32_examples import longest_common
    print(kasai_comparisons("banana"), longest_repeat_k("banana", 2), longest_repeat_k("banana", 3), longest_repeat_k("banana", 4))
    print(longest_common_unchecked("abcabc", "bcx"), longest_common("abcabc", "bcx"))
