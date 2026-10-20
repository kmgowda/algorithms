"""Volume 1, Chapter 34 - Two Pointers.

Run:  python3 ch34_examples.py
"""

from __future__ import annotations


def dedupe_sorted(a: list[int]) -> int:
    """Remove repeats from a sorted list in place; returns how many unique items now lead the list (Figure 34.1)."""
    if not a:
        return 0
    write = 1
    for read in range(1, len(a)):
        if a[read] != a[write - 1]:
            a[write] = a[read]
            write += 1
    return write


def merge_sorted(a: list[int], b: list[int]) -> tuple[list[int], int]:
    """Merge two sorted lists with one pointer in each (Figure 34.2). Returns (merged, comparisons)."""
    i = j = comparisons = 0
    out = []
    while i < len(a) and j < len(b):
        comparisons += 1
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out, comparisons


def best_bookends(h: list[int]) -> tuple[int, list[tuple[int, int, int]]]:
    """Largest (distance x shorter height) over all pairs, moving the shorter end inward (Figure 34.3)."""
    left, right, best, visited = 0, len(h) - 1, 0, []
    while left < right:
        area = (right - left) * min(h[left], h[right])
        visited.append((left, right, area))
        best = max(best, area)
        if h[left] < h[right]:
            left += 1
        else:
            right -= 1
    return best, visited


def common_sorted(a: list[int], b: list[int]) -> list[int]:
    """Members of both sorted lists, with two pointers and no extra memory (Section 34.8)."""
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return out


if __name__ == "__main__":
    s = [12, 12, 25, 31, 31, 31, 47, 63, 63]
    k = dedupe_sorted(s)
    print(s[:k], merge_sorted([12, 31, 58, 84], [25, 47, 63]), best_bookends([3, 7, 2, 6, 4, 8, 5]))
    print(common_sorted([104, 117, 125, 149, 160], [117, 133, 149, 160, 171]))
