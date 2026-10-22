"""Volume 2, Chapter 18 - Thinking Problems.

Problem 2: three prices that sum to the card, in O(n^2) with a sort and two pointers per first price.
Problem 3: the wrong bookends rule that moves the taller end, kept here so the tests can show it.
"""

from __future__ import annotations


def three_for_card(prices: list[int], card: int) -> tuple[int, int, int] | None:
    p = sorted(prices)
    for i in range(len(p) - 2):
        left, right = i + 1, len(p) - 1
        while left < right:
            total = p[i] + p[left] + p[right]
            if total == card:
                return p[i], p[left], p[right]
            if total < card:
                left += 1
            else:
                right -= 1
    return None


def bookends_move_taller(h: list[int]) -> int:
    """WRONG: moves the taller end inward, and can step past the best pair."""
    left, right, best = 0, len(h) - 1, 0
    while left < right:
        best = max(best, (right - left) * min(h[left], h[right]))
        if h[left] > h[right]:
            left += 1
        else:
            right -= 1
    return best


if __name__ == "__main__":
    print(three_for_card([4, 9, 20, 6, 17, 13, 15], 30), bookends_move_taller([1, 5, 5, 2]))
