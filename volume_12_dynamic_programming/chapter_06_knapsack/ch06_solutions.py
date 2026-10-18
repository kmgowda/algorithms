"""Volume 12, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations


def target_sum_ways(nums: list[int], target: int) -> int:
    """Exercise 1 (LeetCode 494): put + or - before each number to reach target. Count the ways.
    If P is the plus-group: P - (total - P) = target, so P = (total + target) / 2 - count subsets with that sum."""
    total = sum(nums)
    if (total + target) % 2 or abs(target) > total:
        return 0
    goal = (total + target) // 2
    ways = [1] + [0] * goal
    for x in nums:
        for s in range(goal, x - 1, -1):
            ways[s] += ways[s - x]
    return ways[goal]


def last_stone_weight(stones: list[int]) -> int:
    """Exercise 2 (LeetCode 1049): smash stones pairwise; smallest possible leftover.
    Equivalent to splitting into two groups as evenly as possible."""
    total = sum(stones)
    reach = {0}
    for s in stones:
        reach |= {r + s for r in reach}
    return min(abs(total - 2 * r) for r in reach)


def bounded_knapsack(items: list[tuple[int, int, int]], capacity: int) -> int:
    """Exercise 3: item i has weight w, value v and only k copies - treat copies as separate 0/1 items."""
    best = [0] * (capacity + 1)
    for w, v, k in items:
        for _ in range(k):
            for c in range(capacity, w - 1, -1):
                best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def ones_and_zeroes(strs: list[str], zeros: int, ones: int) -> int:
    """Exercise 4 (LeetCode 474): most strings using at most m zeros and n ones - a knapsack with TWO capacities."""
    best = [[0] * (ones + 1) for _ in range(zeros + 1)]
    for s in strs:
        z, o = s.count("0"), s.count("1")
        for a in range(zeros, z - 1, -1):
            for b in range(ones, o - 1, -1):
                best[a][b] = max(best[a][b], best[a - z][b - o] + 1)
    return best[zeros][ones]


if __name__ == "__main__":
    print(target_sum_ways([1, 1, 1, 1, 1], 3), last_stone_weight([2, 7, 4, 1, 8, 1]),
          bounded_knapsack([(2, 3, 2), (3, 4, 1)], 7), ones_and_zeroes(["10", "0001", "111001", "1", "0"], 5, 3))
