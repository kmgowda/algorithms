"""Volume 4, Chapter 4 - Hashing Patterns: Complements, Subarray Sums, Streaks.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations


def two_sum(prices: list[int], budget: int) -> tuple[int, int] | None:
    """Pattern 1 - complement lookup (LeetCode 1): remember what you've seen, ask for what you need."""
    seen: dict[int, int] = {}
    for i, price in enumerate(prices):
        if budget - price in seen:
            return seen[budget - price], i
        seen[price] = i
    return None


def count_pairs_with_difference(values: list[int], k: int) -> int:
    """Pattern 1 variant: how many earlier items differ from this one by exactly k? (k > 0)"""
    counts: dict[int, int] = {}
    total = 0
    for v in values:
        total += counts.get(v - k, 0) + counts.get(v + k, 0)
        counts[v] = counts.get(v, 0) + 1
    return total


def subarrays_with_sum(values: list[int], target: int) -> int:
    """Pattern 2 - prefix sums + hash (LeetCode 560): count contiguous runs adding up to target.

    sum(i..j) = prefix[j+1] - prefix[i], so we need earlier prefixes equal to (current - target).
    Works with negative numbers, unlike a sliding window.
    """
    seen_prefix = {0: 1}
    running = total = 0
    for v in values:
        running += v
        total += seen_prefix.get(running - target, 0)
        seen_prefix[running] = seen_prefix.get(running, 0) + 1
    return total


def longest_balanced_run(results: list[str]) -> int:
    """Pattern 3 - first-seen index (LeetCode 525 idea): longest run with equal wins ('W') and losses ('L')."""
    first_index = {0: -1}
    balance = best = 0
    for i, r in enumerate(results):
        balance += 1 if r == "W" else -1
        if balance in first_index:
            best = max(best, i - first_index[balance])
        else:
            first_index[balance] = i
    return best


def longest_streak(days: list[int]) -> int:
    """Pattern 4 - set membership (LeetCode 128): longest run of consecutive day numbers, O(n)."""
    present = set(days)
    best = 0
    for d in present:
        if d - 1 not in present:
            length = 1
            while d + length in present:
                length += 1
            best = max(best, length)
    return best


def fraud_pairs(transactions: list[tuple[str, int]], refund_window: int) -> list[tuple[str, int]]:
    """Industry example: a charge followed by an equal refund (negative) on the same card within a window."""
    last_charge: dict[tuple[str, int], int] = {}
    flagged = []
    for t, (card, amount) in enumerate(transactions):
        if amount < 0 and (card, -amount) in last_charge and t - last_charge[(card, -amount)] <= refund_window:
            flagged.append((card, -amount))
        elif amount > 0:
            last_charge[(card, amount)] = t
    return flagged


if __name__ == "__main__":
    print(two_sum([300, 150, 700, 450], 750), count_pairs_with_difference([1, 5, 3, 4, 2], 2))
    print(subarrays_with_sum([3, 4, -7, 1, 3, 3, 1, -4], 7), longest_balanced_run(list("WLLWWWL")))
    print(longest_streak([10, 4, 20, 1, 3, 2, 11, 12]))
    print(fraud_pairs([("c1", 500), ("c2", 80), ("c1", -500), ("c2", -80)], refund_window=2))
