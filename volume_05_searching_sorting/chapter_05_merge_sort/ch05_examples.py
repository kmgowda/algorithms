"""Volume 5, Chapter 5 - Merge Sort: Divide, Sort, and Merge.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations


def merge(left: list, right: list) -> list:
    """Combine two sorted lists into one sorted list. Takes from the LEFT on ties, which keeps it stable."""
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def merge_sort(items: list) -> list:
    """Top-down: split in half, sort each half recursively, merge. T(n) = 2T(n/2) + n = O(n log n) (V2-C10)."""
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    return merge(merge_sort(items[:mid]), merge_sort(items[mid:]))


def merge_sort_bottom_up(items: list) -> list:
    """No recursion: merge runs of width 1, then 2, 4, 8, ... until one run remains."""
    runs = [[x] for x in items]
    while len(runs) > 1:
        runs = [merge(runs[i], runs[i + 1]) if i + 1 < len(runs) else runs[i] for i in range(0, len(runs), 2)]
    return runs[0] if runs else []


def sort_and_count_inversions(items: list) -> tuple[list, int]:
    """Count pairs i < j with items[i] > items[j] in O(n log n).

    During a merge, when an item from the RIGHT half goes first, it jumps ahead of every item
    still waiting in the left half - each of those is one inversion.
    """
    if len(items) <= 1:
        return list(items), 0
    mid = len(items) // 2
    left, a = sort_and_count_inversions(items[:mid])
    right, b = sort_and_count_inversions(items[mid:])
    out, i, j, crossed = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            crossed += len(left) - i
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out, a + b + crossed


def ranking_disagreement(ranking_a: list[str], ranking_b: list[str]) -> int:
    """Industry example: how differently two judges (or two recommendation models) ranked the same items.
    Count pairs they ordered differently (Kendall tau distance) using inversions."""
    position_in_b = {item: i for i, item in enumerate(ranking_b)}
    return sort_and_count_inversions([position_in_b[item] for item in ranking_a])[1]


def merge_log_files(*logs: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Industry example: each server's log is sorted by time; combine them into one timeline."""
    combined: list[tuple[int, str]] = []
    for log in logs:
        combined = merge(combined, log)
    return combined


if __name__ == "__main__":
    hand = [38, 27, 43, 3, 9, 82, 10]
    print(merge([3, 27, 38, 43], [9, 10, 82]), merge_sort(hand), merge_sort_bottom_up(hand))
    print(sort_and_count_inversions([2, 4, 1, 3, 5]))
    print("Judges disagree on", ranking_disagreement(["lion", "tiger", "zebra", "panda"], ["tiger", "lion", "panda", "zebra"]), "pairs")
    print(merge_log_files([(1, "web: start"), (5, "web: login")], [(2, "db: ready"), (6, "db: query")], [(3, "cache: warm")]))
