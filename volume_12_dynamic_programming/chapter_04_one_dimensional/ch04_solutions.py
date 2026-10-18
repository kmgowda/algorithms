"""Volume 12, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations


def max_subarray(values: list[int]) -> int:
    """Exercise 1 (LeetCode 53): best sum of a contiguous stretch - Kadane (V10-C1) as a 1-D DP."""
    best = cur = values[0]
    for v in values[1:]:
        cur = max(v, cur + v)
        best = max(best, cur)
    return best


def decode_count(digits: str) -> int:
    """Exercise 2 (LeetCode 91): 'A'=1 ... 'Z'=26; how many ways to decode a digit string?
    ways[i] = ways[i-1] if the last digit is 1-9, plus ways[i-2] if the last two form 10-26."""
    ways = [1] + [0] * len(digits)
    for i in range(1, len(digits) + 1):
        if digits[i - 1] != "0":
            ways[i] += ways[i - 1]
        if i >= 2 and 10 <= int(digits[i - 2:i]) <= 26:
            ways[i] += ways[i - 2]
    return ways[len(digits)]


def perfect_squares(n: int) -> int:
    """Exercise 3 (LeetCode 279): fewest perfect squares adding to n - coin change with square coins."""
    squares = [k * k for k in range(1, int(n ** 0.5) + 1)]
    fewest = [0] + [n] * n
    for a in range(1, n + 1):
        fewest[a] = 1 + min(fewest[a - s] for s in squares if s <= a)
    return fewest[n]


def lis_sequence(values: list[int]) -> list[int]:
    """Exercise 4: return an actual longest increasing subsequence, not just its length (parent pointers)."""
    if not values:
        return []
    ending, parent = [1] * len(values), [-1] * len(values)
    for i in range(len(values)):
        for j in range(i):
            if values[j] < values[i] and ending[j] + 1 > ending[i]:
                ending[i], parent[i] = ending[j] + 1, j
    i = max(range(len(values)), key=lambda k: ending[k])
    out = []
    while i != -1:
        out.append(values[i])
        i = parent[i]
    return out[::-1]


if __name__ == "__main__":
    print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), decode_count("226"), perfect_squares(12),
          lis_sequence([10, 9, 2, 5, 3, 7, 101, 18]))
