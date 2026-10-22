"""Volume 2, Chapter 1 - What Is a Data Structure?

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


def operation_costs(shelf: list[int], target: int) -> dict[str, int]:
    """Steps for the operations of Figure 1.2 on a sorted array, counted in the cost model of Volume 1, Chapter 6."""
    linear = next((i + 1 for i, book in enumerate(shelf) if book == target), len(shelf))
    binary, low, high = 0, 0, len(shelf) - 1
    while low <= high:
        mid = (low + high) // 2
        binary += 1
        if shelf[mid] == target:
            break
        if shelf[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return {"read position k": 1, "linear search": linear, "binary search": binary,
            "append": 1, "insert at front": len(shelf)}


if __name__ == "__main__":
    print(operation_costs(SHELF, 63))
    print(operation_costs(list(range(1_000_000)), 999_999))
