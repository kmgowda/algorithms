"""Volume 10, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations


def count_occurrences(values: list[int], target: int) -> int:
    """Exercise 1: count a value by divide and conquer (combine = add)."""
    if not values:
        return 0
    if len(values) == 1:
        return int(values[0] == target)
    mid = len(values) // 2
    return count_occurrences(values[:mid], target) + count_occurrences(values[mid:], target)


def is_sorted_dc(values: list[int]) -> bool:
    """Exercise 2: both halves sorted AND the boundary in order."""
    if len(values) <= 1:
        return True
    mid = len(values) // 2
    return is_sorted_dc(values[:mid]) and is_sorted_dc(values[mid:]) and values[mid - 1] <= values[mid]


def tree_height_dc(tree: dict | None) -> int:
    """Exercise 3: a binary tree's height - the tree splits itself into left and right (V6-C4)."""
    if tree is None:
        return 0
    return 1 + max(tree_height_dc(tree.get("left")), tree_height_dc(tree.get("right")))


def three_way_merge_sort(values: list[int]) -> list[int]:
    """Exercise 4: split into THREE parts. T(n) = 3T(n/3) + n - still O(n log n)."""
    if len(values) <= 1:
        return list(values)
    k = max(1, len(values) // 3)
    parts = [three_way_merge_sort(values[:k]), three_way_merge_sort(values[k:2 * k]), three_way_merge_sort(values[2 * k:])]
    out = []
    while any(parts):
        best = min((p for p in parts if p), key=lambda p: p[0])
        out.append(best.pop(0))
    return out


if __name__ == "__main__":
    print(count_occurrences([1, 3, 1, 2, 1], 1), is_sorted_dc([1, 2, 2, 5]), is_sorted_dc([3, 1]),
          tree_height_dc({"left": {"left": None, "right": None}, "right": None}), three_way_merge_sort([5, 2, 9, 1, 7, 3, 8]))
