"""Volume 2, Chapter 4 - Best, Worst, and Average Case.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

import random


# ------------------------------------------------------------------ linear search, three ways
def comparisons_to_find(items: list[str], target: str) -> int:
    """How many comparisons linear search makes (n if the target is missing)."""
    for count, item in enumerate(items, start=1):
        if item == target:
            return count
    return len(items)


def average_comparisons_exact(n: int) -> float:
    """Average over all n equally likely positions of a target that IS present: (n + 1) / 2."""
    return sum(range(1, n + 1)) / n


def expected_comparisons(probabilities: list[float], missing_probability: float = 0.0) -> float:
    """Expected cost = sum over positions of (cost at that position) x (chance the target is there).

    probabilities[i] is the chance the target is at index i (cost i + 1).
    A missing target costs n comparisons.
    """
    total = sum(probabilities) + missing_probability
    if abs(total - 1.0) > 1e-9:
        raise ValueError("probabilities must add up to 1")
    n = len(probabilities)
    present = sum((i + 1) * p for i, p in enumerate(probabilities))
    return present + missing_probability * n


def simulated_average(n: int, trials: int, seed: int = 0) -> float:
    """Average comparisons over many random searches for a present target (should approach (n+1)/2)."""
    rng = random.Random(seed)
    items = [f"book{i}" for i in range(n)]
    total = 0
    for _ in range(trials):
        total += comparisons_to_find(items, items[rng.randrange(n)])
    return total / trials


# ------------------------------------------------------------------ inserting a card into a sorted hand
def insert_card(hand: list[int], card: int) -> tuple[list[int], int]:
    """Insert into a sorted hand from the right, counting how many cards slide over.

    Best case: the new card is the largest -> 0 shifts.
    Worst case: the new card is the smallest -> len(hand) shifts.
    """
    new_hand = hand + [card]
    shifts = 0
    position = len(new_hand) - 1
    while position > 0 and new_hand[position - 1] > card:
        new_hand[position] = new_hand[position - 1]
        position -= 1
        shifts += 1
    new_hand[position] = card
    return new_hand, shifts


# ------------------------------------------------------------------ duplicate check with early exit
def first_duplicate_comparisons(items: list[int]) -> int:
    """Pair-by-pair duplicate check; returns comparisons used before stopping."""
    comparisons = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            comparisons += 1
            if items[i] == items[j]:
                return comparisons
    return comparisons


# ------------------------------------------------------------------ industry: caches and popular items
def expected_latency(hit_rate: float, hit_ms: float, miss_ms: float) -> float:
    """Industry example: average response time of a system with a cache."""
    if not 0.0 <= hit_rate <= 1.0:
        raise ValueError("hit rate must be between 0 and 1")
    return hit_rate * hit_ms + (1 - hit_rate) * miss_ms


def total_cost_move_to_front(shelf: list[str], requests: list[str]) -> tuple[int, int]:
    """Practical example: a librarian who moves each requested book to the front of the shelf.

    Returns (comparisons with a fixed shelf, comparisons with move-to-front).
    Popular books drift to the front, so the AVERAGE search gets cheaper.
    """
    fixed_cost = sum(comparisons_to_find(shelf, book) for book in requests)
    moving = list(shelf)
    moving_cost = 0
    for book in requests:
        moving_cost += comparisons_to_find(moving, book)
        if book in moving:
            moving.remove(book)
            moving.insert(0, book)
    return fixed_cost, moving_cost


if __name__ == "__main__":
    shelf = ["Atlas", "Birds", "Cats", "Dune", "Emma"]
    print("Best, middle, worst:", [comparisons_to_find(shelf, t) for t in ("Atlas", "Cats", "Zebra")])
    print("Exact average for n=5:", average_comparisons_exact(5))
    print("Simulated average for n=100:", simulated_average(100, 20_000))
    popular_first = [0.5, 0.2, 0.15, 0.1, 0.05]
    print("Expected when popular books come first:", expected_comparisons(popular_first))
    print("Insert 9 into [2,5,7]:", insert_card([2, 5, 7], 9), "| insert 1:", insert_card([2, 5, 7], 1))
    print("Cache latency at 90% hits:", round(expected_latency(0.9, 2, 80), 2), "ms")
    requests = ["Emma"] * 8 + ["Dune"] * 4 + ["Atlas"]
    print("Fixed vs move-to-front:", total_cost_move_to_front(shelf, requests))
