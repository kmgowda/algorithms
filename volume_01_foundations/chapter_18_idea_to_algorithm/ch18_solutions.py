"""Volume 1, Chapter 18, Thinking Problem 2 - spend as much of the gift card as possible.

When no two books cost exactly the card's value, find two different books whose prices add up to as much as possible
without going over it. Two pointers on sorted prices do it in at most n - 1 checks.

Run:  python3 ch18_solutions.py
"""

from __future__ import annotations


def best_pair_at_most(prices: list[int], target: int) -> tuple[int, int] | None:
    """Positions of two books (sorted prices) with the largest total <= target, or None if no pair fits."""
    left, right, best = 0, len(prices) - 1, None
    while left < right:
        total = prices[left] + prices[right]
        if total > target:
            right -= 1
        else:
            if best is None or total > prices[best[0]] + prices[best[1]]:
                best = (left, right)
            left += 1
    return best


if __name__ == "__main__":
    shelf = [4, 6, 9, 13, 15, 17, 20]
    for card in (27, 30, 9, 10, 100):
        print(card, best_pair_at_most(shelf, card))
