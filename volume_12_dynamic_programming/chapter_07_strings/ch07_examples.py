"""Volume 12, Chapter 7 - DP on Strings: Palindromes, Word Break.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations


def palindrome_table(s: str) -> list[list[bool]]:
    """is_pal[i][j]: is s[i..j] a palindrome? True when the ends match and the inside is a palindrome.
    Fill by increasing length, so the inside (shorter) is always ready."""
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = s[i] == s[j] and (length <= 2 or is_pal[i + 1][j - 1])
    return is_pal


def count_palindromic_substrings(s: str) -> int:
    """LeetCode 647: how many substrings (by position) are palindromes."""
    return sum(row.count(True) for row in palindrome_table(s))


def longest_palindromic_substring(s: str) -> str:
    """LeetCode 5: the longest contiguous palindrome."""
    best = ""
    table = palindrome_table(s)
    for i in range(len(s)):
        for j in range(i, len(s)):
            if table[i][j] and j - i + 1 > len(best):
                best = s[i:j + 1]
    return best


def longest_palindromic_subsequence(s: str) -> int:
    """LeetCode 516: longest palindrome keeping order but allowing gaps.
    L[i][j] = L[i+1][j-1] + 2 if the ends match, else max(L[i+1][j], L[i][j-1])."""
    n = len(s)
    L = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        L[i][i] = 1
        for j in range(i + 1, n):
            L[i][j] = L[i + 1][j - 1] + 2 if s[i] == s[j] else max(L[i + 1][j], L[i][j - 1])
    return L[0][n - 1] if n else 0


def word_break(text: str, words: list[str]) -> bool:
    """LeetCode 139: can the text be split into dictionary words? ok[i] = some word ends at i after an ok[j]."""
    vocab, longest = set(words), max(map(len, words), default=0)
    ok = [True] + [False] * len(text)
    for i in range(1, len(text) + 1):
        for j in range(max(0, i - longest), i):
            if ok[j] and text[j:i] in vocab:
                ok[i] = True
                break
    return ok[len(text)]


def segment_hashtag(tag: str, words: list[str]) -> list[str] | None:
    """Industry example: split '#bestpizzainmumbai' into words, preferring FEWER, longer words (search engines do this)."""
    vocab = set(words)
    best: list[list[str] | None] = [[]] + [None] * len(tag)
    for i in range(1, len(tag) + 1):
        for j in range(i):
            piece = tag[j:i]
            if best[j] is not None and piece in vocab:
                candidate = best[j] + [piece]                 # type: ignore[operator]
                if best[i] is None or len(candidate) < len(best[i]):  # type: ignore[arg-type]
                    best[i] = candidate
    return best[len(tag)]


if __name__ == "__main__":
    print(count_palindromic_substrings("aaa"), longest_palindromic_substring("forgeeksskeegfor"),
          longest_palindromic_subsequence("bbbab"))
    print(word_break("applepenapple", ["apple", "pen"]), word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))
    print(segment_hashtag("bestpizzainmumbai", ["best", "pizza", "in", "mumbai", "be", "st", "pi", "zza", "mum", "bai"]))
