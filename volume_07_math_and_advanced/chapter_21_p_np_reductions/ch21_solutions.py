"""Volume 7, Chapter 21 - Thinking Problems.

Problem 1: reductions compose: applying two fast, answer-preserving translations in a row is again one.
Problem 2: finding a subset with only a yes/no oracle: n + 1 oracle calls.
Problem 3: the reduction-direction flaw: sorting reduces to SAT too, yet sorting is easy (illustrated in the text).
"""

from __future__ import annotations

from ch21_examples import find_subset


def decide(prices: list, target: int, calls: list) -> bool:
    """The yes/no oracle: does some choice of these prices total exactly target?"""
    calls[0] += 1
    return find_subset(prices, target)[0] is not None


def find_with_oracle(prices: list, target: int) -> tuple[list | None, int]:
    """Self-reduction: try dropping each book; keep it only if the answer would become no. Returns (indices, calls)."""
    calls = [0]
    if not decide(prices, target, calls):
        return None, calls[0]
    kept = list(range(len(prices)))
    for i in range(len(prices)):
        trial = [j for j in kept if j != i]
        if decide([prices[j] for j in trial], target, calls):
            kept = trial                        # book i is not needed
    return kept, calls[0]


def scale(prices: list, target: int, k: int) -> tuple[list, int]:
    """A tiny reduction from subset sum to subset sum (k >= 1): multiply every price and the target by k.
    The answer is unchanged, and the translation takes O(n) steps."""
    return [p * k for p in prices], target * k


if __name__ == "__main__":
    from ch21_examples import PRICES
    print(find_with_oracle(PRICES, 31), find_with_oracle(PRICES, 200), find_with_oracle([], 0))
