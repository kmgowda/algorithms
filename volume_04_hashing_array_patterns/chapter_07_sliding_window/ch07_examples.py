"""Volume 4, Chapter 7 - Sliding Window: Fixed and Variable Windows.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations


def best_k_day_sales(sales: list[int], k: int) -> int:
    """Fixed window (LeetCode 643 idea): the best total over k consecutive days. Add the new day, drop the old."""
    if not 0 < k <= len(sales):
        raise ValueError("need 0 < k <= len(sales)")
    window = sum(sales[:k])
    best = window
    for i in range(k, len(sales)):
        window += sales[i] - sales[i - k]
        best = max(best, window)
    return best


def longest_unique_run(text: str) -> int:
    """Variable window (LeetCode 3): the longest stretch with no repeated character.

    Grow on the right; when a repeat appears, jump the left edge past its previous position.
    """
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(text):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


def shortest_run_reaching(values: list[int], target: int) -> int:
    """Variable window (LeetCode 209): shortest stretch with sum >= target (values are positive). 0 if none."""
    left = total = 0
    best = len(values) + 1
    for right, v in enumerate(values):
        total += v
        while total >= target:
            best = min(best, right - left + 1)
            total -= values[left]
            left += 1
    return best if best <= len(values) else 0


def fruit_baskets(trees: list[str]) -> int:
    """Variable window (LeetCode 904): longest stretch of trees with at most 2 kinds of fruit."""
    counts: dict[str, int] = {}
    left = best = 0
    for right, fruit in enumerate(trees):
        counts[fruit] = counts.get(fruit, 0) + 1
        while len(counts) > 2:
            counts[trees[left]] -= 1
            if counts[trees[left]] == 0:
                del counts[trees[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


def error_alerts(error_times: list[int], window: int, threshold: int) -> list[int]:
    """Industry example: alert at each time where more than `threshold` errors happened in the last `window` seconds."""
    alerts = []
    left = 0
    for right, t in enumerate(error_times):
        while error_times[left] <= t - window:
            left += 1
        if right - left + 1 > threshold:
            alerts.append(t)
    return alerts


if __name__ == "__main__":
    print(best_k_day_sales([120, 80, 200, 150, 90, 300, 60], 3))
    print(longest_unique_run("abcabcbb"), longest_unique_run("zoozebra"))
    print(shortest_run_reaching([2, 3, 1, 2, 4, 3], 7))
    print(fruit_baskets(["apple", "mango", "apple", "kiwi", "kiwi", "apple", "kiwi"]))
    print(error_alerts([1, 2, 3, 10, 11, 12, 13, 30], window=5, threshold=3))
