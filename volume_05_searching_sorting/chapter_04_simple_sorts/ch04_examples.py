"""Volume 5, Chapter 4 - Simple Sorts: Bubble, Selection, Insertion (Sorting Playing Cards).

Each function sorts a COPY and returns (sorted_list, comparisons, moves) so we can count the work.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

import random


def bubble_sort(items: list) -> tuple[list, int, int]:
    """Swap neighbours that are out of order; the biggest 'bubbles' to the end each pass.
    Stops early if a pass makes no swaps (already sorted). Stable."""
    a = list(items)
    comparisons = swaps = 0
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for i in range(end):
            comparisons += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return a, comparisons, swaps


def selection_sort(items: list) -> tuple[list, int, int]:
    """Find the smallest remaining card and put it next in line. Always n(n-1)/2 comparisons,
    but at most n-1 swaps. Not stable."""
    a = list(items)
    comparisons = swaps = 0
    for i in range(len(a) - 1):
        smallest = i
        for j in range(i + 1, len(a)):
            comparisons += 1
            if a[j] < a[smallest]:
                smallest = j
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
            swaps += 1
    return a, comparisons, swaps


def insertion_sort(items: list) -> tuple[list, int, int]:
    """Take the next card and slide it left into place among the sorted cards in your hand.
    Fast on nearly-sorted input (adaptive). Stable."""
    a = list(items)
    comparisons = shifts = 0
    for i in range(1, len(a)):
        card = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] <= card:
                break
            a[j + 1] = a[j]                 # shift the bigger card right
            shifts += 1
            j -= 1
        a[j + 1] = card
    return a, comparisons, shifts


def work_table(n: int, seed: int = 0) -> dict[str, dict[str, tuple[int, int]]]:
    """Comparisons and moves for random, sorted, and reversed inputs of size n."""
    rng = random.Random(seed)
    inputs = {"random": rng.sample(range(n), n), "sorted": list(range(n)), "reversed": list(range(n, 0, -1))}
    table: dict[str, dict[str, tuple[int, int]]] = {}
    for name, sort in (("bubble", bubble_sort), ("selection", selection_sort), ("insertion", insertion_sort)):
        table[name] = {kind: sort(data)[1:] for kind, data in inputs.items()}
    return table


def add_late_entries(sorted_scores: list[int], late: list[int]) -> list[int]:
    """Industry example: a leaderboard is already sorted; a few late scores arrive. Insertion sort shines."""
    return insertion_sort(sorted_scores + late)[0]


if __name__ == "__main__":
    hand = [7, 2, 9, 4, 3]
    for sort in (bubble_sort, selection_sort, insertion_sort):
        print(f"{sort.__name__:>15}: {sort(hand)}")
    for name, row in work_table(100).items():
        print(f"{name:>10} (comparisons, moves): {row}")
    print(add_late_entries([10, 20, 30, 40, 50, 60], [35, 5]))
