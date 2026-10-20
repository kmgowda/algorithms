"""Volume 1, Chapter 18 - From Idea to Algorithm.

Run:  python3 ch18_examples.py
"""

from __future__ import annotations

import random
import timeit

PRICES = [4, 6, 9, 13, 15, 17, 20]


def pair_brute(prices: list[int], target: int) -> tuple[int, int] | None:
    """Try every pair once (Figure 18.3): O(n^2), the trusted reference."""
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            if prices[i] + prices[j] == target:
                return i, j
    return None


def pair_two_pointers(prices: list[int], target: int) -> tuple[int, int] | None:
    """Positions of two books (sorted prices) summing to target, or None: O(n) steps (Figure 18.4)."""
    left, right = 0, len(prices) - 1
    while left < right:
        total = prices[left] + prices[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None


def agree(prices: list[int], target: int) -> bool:
    """Both methods agree on whether a pair exists, and any pair returned is valid (Figure 18.5)."""
    a, b = pair_brute(prices, target), pair_two_pointers(prices, target)
    if (a is None) != (b is None):
        return False
    return b is None or (b[0] != b[1] and prices[b[0]] + prices[b[1]] == target)


def measure(sizes=(500, 1000, 2000, 4000)) -> list[tuple[int, float, float]]:
    """Milliseconds for both methods with a target that has no answer (Figure 18.6)."""
    rows = []
    for n in sizes:
        prices = sorted(random.Random(n).sample(range(1, 10 ** 6), n))
        brute = min(timeit.repeat(lambda: pair_brute(prices, -1), number=1, repeat=3)) * 1000
        fast = min(timeit.repeat(lambda: pair_two_pointers(prices, -1), number=5, repeat=3)) / 5 * 1000
        rows.append((n, round(brute, 2), round(fast, 3)))
    return rows


if __name__ == "__main__":
    print(pair_brute(PRICES, 30), pair_two_pointers(PRICES, 30), pair_two_pointers(PRICES, 35),
          pair_two_pointers(PRICES, 100))
    rng = random.Random(1)
    print(all(agree(sorted(rng.randint(1, 30) for _ in range(rng.randint(0, 12))), rng.randint(0, 60))
              for _ in range(1000)))
    for row in measure():
        print(row)
