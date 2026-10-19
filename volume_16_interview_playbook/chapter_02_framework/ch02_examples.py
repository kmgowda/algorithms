"""Volume 16, Chapter 2 - The Problem-Solving Framework Revisited.

One problem (LeetCode 1, Two Sum) taken through every step: understand, examples, brute force, improve,
code, test, analyse.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import random

FRAMEWORK = ["understand", "examples", "brute force", "improve", "code", "test", "analyse"]

CLARIFYING_QUESTIONS = [
    "What is the input size and value range?",
    "Can values repeat or be negative?",
    "Is there always exactly one answer? What if there is none?",
    "Return values or indices? Does order matter?",
    "Can I modify the input?",
]


def two_sum_brute(nums: list[int], target: int) -> list[int] | None:
    """Step 3, brute force: try every pair. O(n^2) time, O(1) memory - always state it first."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return None


def two_sum(nums: list[int], target: int) -> list[int] | None:
    """Step 4, improve: 'for each x, have I already seen target - x?' is a look-up question -> hash map.
    O(n) time, O(n) memory."""
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return None


def edge_cases() -> list[tuple[list[int], int]]:
    """Step 6, test: small, tricky inputs to trace by hand."""
    return [
        ([2, 7, 11, 15], 9),          # the given example
        ([3, 3], 6),                  # duplicates
        ([-1, -2, -3, -4], -6),       # negatives
        ([0, 4, 3, 0], 0),            # zeros
        ([1, 2], 7),                  # no answer
    ]


def random_check(trials: int, rng: random.Random) -> bool:
    """Compare the fast solution with the brute force on random inputs (Chapter 10 grows this into a habit)."""
    for _ in range(trials):
        nums = [rng.randint(-10, 10) for _ in range(rng.randint(0, 8))]
        t = rng.randint(-15, 15)
        fast, slow = two_sum(nums, t), two_sum_brute(nums, t)
        if (fast is None) != (slow is None):
            return False
        if fast is not None and nums[fast[0]] + nums[fast[1]] != t:
            return False
    return True


def walkthrough(nums: list[int], target: int) -> list[str]:
    """What to SAY while tracing the hash-map solution on an example."""
    seen: dict[int, int] = {}
    lines = []
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            lines.append(f"i={i}, x={x}: need {need}, seen at {seen[need]} -> answer [{seen[need]}, {i}]")
            break
        seen[x] = i
        lines.append(f"i={i}, x={x}: need {need}, not seen; store {x}->{i}")
    return lines


if __name__ == "__main__":
    print(" -> ".join(FRAMEWORK))
    print(two_sum_brute([2, 7, 11, 15], 9), two_sum([2, 7, 11, 15], 9))
    print([two_sum(n, t) for n, t in edge_cases()])
    print("random check:", random_check(500, random.Random(1)))
    print("\n".join(walkthrough([3, 2, 4], 6)))
