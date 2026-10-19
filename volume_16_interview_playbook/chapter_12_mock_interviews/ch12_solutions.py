"""Volume 16, Chapter 12 - Solutions to the exercises."""

from __future__ import annotations

from functools import lru_cache


def three_sum_closest(nums: list[int], target: int) -> int:
    """Exercise 1 (LeetCode 16): the same sort + two pointers, tracking the closest sum instead of exact zeros."""
    nums = sorted(nums)
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if abs(s - target) < abs(best - target):
                best = s
            if s < target:
                lo += 1
            elif s > target:
                hi -= 1
            else:
                return s
    return best


def word_break_all(s: str, words: list[str]) -> list[str]:
    """Exercise 2 (LeetCode 140): every sentence - memoized backtracking over suffixes."""
    vocab = set(words)

    @lru_cache(maxsize=None)
    def go(start: int) -> tuple[str, ...]:
        if start == len(s):
            return ("",)
        out = []
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in vocab:
                out.extend((s[start:end] + " " + rest).strip() for rest in go(end))
        return tuple(out)

    return sorted(go(0))


def self_review(notes: dict[str, bool]) -> list[str]:
    """Exercise 3: after a mock, list the framework steps you skipped (Chapter 2's checklist)."""
    steps = ["clarified", "gave examples", "stated brute force", "explained improvement", "tested", "gave complexity"]
    return [s for s in steps if not notes.get(s, False)]


if __name__ == "__main__":
    print(three_sum_closest([-1, 2, 1, -4], 1), word_break_all("catsanddog", ["cat", "cats", "and", "sand", "dog"]),
          self_review({"clarified": True, "tested": False}))
