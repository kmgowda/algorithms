"""Volume 4, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

from collections import Counter


def longest_ones_with_flips(bits: list[int], k: int) -> int:
    """Exercise 1 (LeetCode 1004): longest run of 1s if you may flip at most k zeros."""
    left = zeros = best = 0
    for right, b in enumerate(bits):
        zeros += b == 0
        while zeros > k:
            zeros -= bits[left] == 0
            left += 1
        best = max(best, right - left + 1)
    return best


def anagram_positions(text: str, word: str) -> list[int]:
    """Exercise 2 (LeetCode 438): start positions where an anagram of word appears. Fixed window of counts."""
    k = len(word)
    if k > len(text):
        return []
    need, window = Counter(word), Counter(text[:k])
    out = [0] if window == need else []
    for i in range(k, len(text)):
        window[text[i]] += 1
        window[text[i - k]] -= 1
        if window[text[i - k]] == 0:
            del window[text[i - k]]
        if window == need:
            out.append(i - k + 1)
    return out


def smallest_covering_window(text: str, letters: str) -> str:
    """Exercise 3 (LeetCode 76): the shortest stretch of text containing all of `letters` (with repeats)."""
    need = Counter(letters)
    missing = len(letters)
    left = 0
    best = (0, len(text) + 1)
    for right, ch in enumerate(text, 1):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while need[text[left]] < 0:
                need[text[left]] += 1
                left += 1
            if right - left < best[1] - best[0]:
                best = (left, right)
            need[text[left]] += 1
            missing += 1
            left += 1
    return text[best[0]:best[1]] if best[1] <= len(text) else ""


def max_average(values: list[float], k: int) -> float:
    """Exercise 4 (LeetCode 643): best average of k consecutive values."""
    window = sum(values[:k])
    best = window
    for i in range(k, len(values)):
        window += values[i] - values[i - k]
        best = max(best, window)
    return best / k


if __name__ == "__main__":
    print(longest_ones_with_flips([1, 1, 0, 0, 1, 1, 1, 0, 1], 1), anagram_positions("cbaebabacd", "abc"))
    print(smallest_covering_window("ADOBECODEBANC", "ABC"), max_average([1, 12, -5, -6, 50, 3], 4))
