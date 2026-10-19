"""Volume 16, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

import heapq


def min_jumps(nums: list[int]) -> int:
    """Exercise 1 (LeetCode 45): BFS-like greedy - each 'level' is the range reachable with one more jump."""
    jumps = current_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
    return jumps


def gas_station(gas: list[int], cost: list[int]) -> int:
    """Exercise 2 (LeetCode 134): if total gas >= total cost, the start is just after the last point where the
    running tank went negative."""
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        tank += g - c
        if tank < 0:
            start, tank = i + 1, 0
    return start


def k_closest(points: list[tuple[int, int]], k: int) -> list[tuple[int, int]]:
    """Exercise 3 (LeetCode 973): the k points nearest the origin with a heap."""
    return sorted(heapq.nsmallest(k, points, key=lambda p: p[0] * p[0] + p[1] * p[1]))


if __name__ == "__main__":
    print(min_jumps([2, 3, 1, 1, 4]), gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), k_closest([(1, 3), (-2, 2), (5, 8)], 1))
