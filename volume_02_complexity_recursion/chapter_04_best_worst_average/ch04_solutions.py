"""Volume 2, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations

from itertools import permutations

from ch04_examples import comparisons_to_find, expected_comparisons, expected_latency, insert_card


def cases_for_find_max(n: int) -> tuple[int, int]:
    """Exercise 1: finding the max always compares n - 1 times: best = worst."""
    return n - 1, n - 1


def average_shifts_over_all_orders(hand_size: int) -> float:
    """Exercise 3: average shifts when inserting each new card in every possible arrival order.

    Builds a hand one card at a time from cards 1..hand_size, for every ordering, and averages
    the total shifts. The exact answer is hand_size * (hand_size - 1) / 4.
    """
    orders = list(permutations(range(1, hand_size + 1)))
    total = 0
    for order in orders:
        hand: list[int] = []
        for card in order:
            hand, shifts = insert_card(hand, card)
            total += shifts
    return total / len(orders)


def expected_with_missing(n: int, chance_missing: float) -> float:
    """Exercise 4: present targets are equally likely anywhere; sometimes the target is missing."""
    present_each = (1 - chance_missing) / n
    return expected_comparisons([present_each] * n, chance_missing)


def break_even_hit_rate(hit_ms: float, miss_ms: float, budget_ms: float) -> float:
    """Exercise 5: the lowest cache hit rate that keeps average latency within budget."""
    if budget_ms >= miss_ms:
        return 0.0
    if budget_ms < hit_ms:
        raise ValueError("budget is below even the cache-hit time")
    rate = (miss_ms - budget_ms) / (miss_ms - hit_ms)
    assert expected_latency(rate, hit_ms, miss_ms) <= budget_ms + 1e-9
    return rate


def worst_input_for_search(items: list[str]) -> str:
    """Exercise 6: an adversary picks a target that is not on the shelf."""
    candidate = "zzz"
    while candidate in items:
        candidate += "z"
    assert comparisons_to_find(items, candidate) == len(items)
    return candidate


if __name__ == "__main__":
    print(cases_for_find_max(10), average_shifts_over_all_orders(5), expected_with_missing(10, 0.5))
    print(break_even_hit_rate(2, 80, 10), worst_input_for_search(["a", "zzz"]))
