"""Volume 6, Chapter 33 - Thinking Problems.

Problem 1: a centre of the #-string with radius r holds exactly (r + 1) // 2 palindromes (checked by brute force).
Problem 2: the fewest letters to add at the front to make a palindrome, with Chapter 26's border table.
Problem 3: growing only from letters (odd centres) misses every even palindrome, such as "noon".
"""

from __future__ import annotations

import importlib.util
import os

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("ch26_v6", os.path.join(_here, "..", "chapter_26_kmp", "ch26_examples.py"))
_kmp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_kmp)


def brute_count(s: str) -> int:
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])


def shortest_front_palindrome(s: str) -> str:
    """Longest palindromic beginning of s = longest border of s + sep + reversed(s); add the rest, reversed, in front."""
    if not s:
        return ""
    keep = _kmp.failure(s + "\0" + s[::-1])[-1]
    return s[keep:][::-1] + s


def odd_only(s: str) -> str:
    best = ""
    for c in range(len(s)):
        lo = hi = c
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            lo, hi = lo - 1, hi + 1
        if hi - lo - 1 > len(best):
            best = s[lo + 1:hi]
    return best


if __name__ == "__main__":
    from ch33_examples import count_palindromes, expand_around_centres
    print(count_palindromes("abacabad"), brute_count("abacabad"), shortest_front_palindrome("abcd"), shortest_front_palindrome("aacecaaa"))
    print(odd_only("noon"), expand_around_centres("noon")[0])
