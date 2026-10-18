"""Volume 13, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

from ch10_examples import choose_matcher


def pick_matchers() -> dict[str, str]:
    """Exercise 1: choose a matcher for each job."""
    return {
        "block 5,000 banned chat words": choose_matcher({"many patterns"}),
        "answer a million probe lookups on one genome": choose_matcher({"one text, many queries"}),
        "scan a live network stream for one signature": choose_matcher({"stream or guaranteed linear time"}),
        "find a long phrase in a novel": choose_matcher({"long pattern, varied text"}),
        "find near-duplicate essays": choose_matcher({"same-length patterns or document fingerprints"}),
        "longest palindrome in a DNA read": choose_matcher({"palindromes"}),
        "find a word in a short email": choose_matcher(set()),
    }


def break_even_queries(build_ms: float, query_ms: float, scan_ms: float) -> int:
    """Exercise 2: after how many queries does building a suffix array beat scanning the text every time?"""
    if scan_ms <= query_ms:
        return -1
    k = 1
    while build_ms + k * query_ms >= k * scan_ms:
        k += 1
    return k


if __name__ == "__main__":
    print(pick_matchers())
    print(break_even_queries(24.2, 0.003, 1.0))
