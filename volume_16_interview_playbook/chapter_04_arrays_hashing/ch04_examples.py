"""Volume 16, Chapter 4 - Arrays, Strings, and Hashing: Interview Drill.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

from collections import Counter, defaultdict


def group_anagrams(words: list[str]) -> list[list[str]]:
    """LeetCode 49: words with the same sorted letters share a key. O(total letters x log word length)."""
    groups: dict[str, list[str]] = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return sorted(sorted(g) for g in groups.values())


def longest_consecutive(nums: list[int]) -> int:
    """LeetCode 128: longest run of consecutive integers in O(n) - only start counting at a run's first number."""
    present, best = set(nums), 0
    for x in present:
        if x - 1 not in present:
            length = 1
            while x + length in present:
                length += 1
            best = max(best, length)
    return best


def product_except_self(nums: list[int]) -> list[int]:
    """LeetCode 238: without division - multiply the product of everything to the left by everything to the right."""
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out


def longest_unique_substring(s: str) -> int:
    """LeetCode 3: sliding window - move the left edge past the previous copy of a repeated letter."""
    last: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


def min_window(s: str, t: str) -> str:
    """LeetCode 76: shortest substring of s containing every letter of t (with multiplicity).
    Grow the window until it covers t, then shrink from the left while it still covers."""
    need, missing = Counter(t), len(t)
    left, best = 0, (0, len(s) + 1)
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left < best[1] - best[0]:
                best = (left, right + 1)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return s[best[0]:best[1]] if best[1] <= len(s) else ""


def top_spender_session(amounts: list[int], k: int) -> int:
    """Industry example: the biggest total spent in any k consecutive transactions (fixed sliding window)."""
    window = sum(amounts[:k])
    best = window
    for i in range(k, len(amounts)):
        window += amounts[i] - amounts[i - k]
        best = max(best, window)
    return best


if __name__ == "__main__":
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    print(longest_consecutive([100, 4, 200, 1, 3, 2]), product_except_self([1, 2, 3, 4]))
    print(longest_unique_substring("abcabcbb"), repr(min_window("ADOBECODEBANC", "ABC")))
    print(top_spender_session([20, 5, 40, 10, 30, 5], 3))
