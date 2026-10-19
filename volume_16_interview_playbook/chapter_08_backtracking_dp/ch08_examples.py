"""Volume 16, Chapter 8 - Backtracking and Dynamic Programming: Interview Drill.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

from bisect import bisect_left


def permutations(nums: list[int]) -> list[list[int]]:
    """LeetCode 46: choose an unused number, explore, un-choose (V11-C2)."""
    out, path, used = [], [], [False] * len(nums)

    def go() -> None:
        if len(path) == len(nums):
            out.append(path[:])
            return
        for i, x in enumerate(nums):
            if not used[i]:
                used[i] = True
                path.append(x)
                go()
                path.pop()
                used[i] = False

    go()
    return out


def subsets(nums: list[int]) -> list[list[int]]:
    """LeetCode 78: at each index, every partial path is itself a subset."""
    out, path = [], []

    def go(start: int) -> None:
        out.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            go(i + 1)
            path.pop()

    go(0)
    return out


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """LeetCode 39: reuse allowed, so recurse from the same index; sorted input lets us stop early."""
    out, path = [], []
    cands = sorted(candidates)

    def go(start: int, remaining: int) -> None:
        if remaining == 0:
            out.append(path[:])
            return
        for i in range(start, len(cands)):
            if cands[i] > remaining:
                break
            path.append(cands[i])
            go(i, remaining - cands[i])
            path.pop()

    go(0, target)
    return out


def climb_stairs(n: int) -> int:
    """LeetCode 70: ways(n) = ways(n-1) + ways(n-2), two variables (V12-C4)."""
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def rob(houses: list[int]) -> int:
    """LeetCode 198: take this house plus the best two back, or skip it."""
    take, skip = 0, 0
    for v in houses:
        take, skip = skip + v, max(take, skip)
    return max(take, skip)


def coin_change(coins: list[int], amount: int) -> int:
    """LeetCode 322: fewest coins; dp[a] = 1 + min dp[a - c]."""
    best = [0] + [amount + 1] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                best[a] = min(best[a], best[a - c] + 1)
    return best[amount] if best[amount] <= amount else -1


def length_of_lis(nums: list[int]) -> int:
    """LeetCode 300: tails[k] = smallest tail of an increasing subsequence of length k + 1. O(n log n)."""
    tails: list[int] = []
    for x in nums:
        i = bisect_left(tails, x)
        tails[i:i + 1] = [x]
    return len(tails)


def lcs(a: str, b: str) -> int:
    """LeetCode 1143: longest common subsequence with one rolling row (V12-C12)."""
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0]
        for j, other in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if ch == other else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def fewest_bills(amount: int) -> int:
    """Industry example: an ATM paying out with the fewest notes from denominations that greedy can get wrong."""
    return coin_change([1, 7, 10], amount)


if __name__ == "__main__":
    print(len(permutations([1, 2, 3])), subsets([1, 2]), combination_sum([2, 3, 6, 7], 7))
    print(climb_stairs(5), rob([2, 7, 9, 3, 1]), coin_change([1, 2, 5], 11), coin_change([2], 3))
    print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), lcs("abcde", "ace"), fewest_bills(14))
