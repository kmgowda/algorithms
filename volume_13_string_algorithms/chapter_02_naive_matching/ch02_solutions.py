"""Volume 13, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations


def match_with_wildcards(text: str, pattern: str) -> list[int]:
    """Exercise 1: '?' in the pattern matches any one character - easy with naive matching."""
    m = len(pattern)
    return [i for i in range(len(text) - m + 1)
            if all(p == "?" or p == text[i + j] for j, p in enumerate(pattern))]


def count_matches_with_mismatches(text: str, pattern: str, k: int) -> list[int]:
    """Exercise 2: positions where the pattern matches with at most k differing letters (sequencing errors)."""
    m = len(pattern)
    out = []
    for i in range(len(text) - m + 1):
        diff = 0
        for j in range(m):
            if text[i + j] != pattern[j]:
                diff += 1
                if diff > k:
                    break
        if diff <= k:
            out.append(i)
    return out


def worst_case_formula(n: int, m: int) -> int:
    """Exercise 3: comparisons naive search makes on 'a'*n with 'a'*(m-1)+'b' - every alignment does m."""
    return (n - m + 1) * m


if __name__ == "__main__":
    print(match_with_wildcards("bananas", "a?a"), count_matches_with_mismatches("ACGTACGA", "ACGA", 1),
          worst_case_formula(10000, 50))
