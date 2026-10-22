"""Volume 3, Chapter 3 - Searching Rotated and Two-Dimensional Data.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

ROTATED = [58, 63, 70, 84, 91, 12, 25, 31, 47]     # Maya's shelf, rotated: the end was moved to the front
GRID = [[12, 25, 31, 47],
        [20, 33, 52, 60],
        [27, 41, 66, 74],
        [35, 58, 80, 91]]                            # every row and every column increases


def find_rotation(a: list, trace: list | None = None) -> int:
    """Index of the smallest value (where the rotation starts), by binary search (Section 3.4); 0 for an empty list."""
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if trace is not None:
            trace.append((lo, hi, mid, a[mid], a[hi]))
        if a[mid] > a[hi]:
            lo = mid + 1          # the drop is to the right of mid
        else:
            hi = mid
    return lo


def find_rotation_with_duplicates(a: list) -> int:
    """Like find_rotation, but when a[mid] = a[hi] the drop could be either side: drop hi by one (worst case O(n))."""
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] > a[hi]:
            lo = mid + 1
        elif a[mid] < a[hi]:
            hi = mid
        else:
            hi -= 1
    return lo


def search_rotated(a: list, key, trace: list | None = None) -> int:
    """Binary search on a rotated sorted list: one half is always sorted (Figure 3.3). Returns index or -1."""
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if trace is not None:
            trace.append((lo, hi, mid, a[mid]))
        if a[mid] == key:
            return mid
        if a[lo] <= a[mid]:                       # left half sorted
            if a[lo] <= key < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                     # right half sorted
            if a[mid] < key <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def search_rotated_with_duplicates(a: list, key) -> int:
    """Section 3.7: when a[lo] = a[mid] = a[hi] the drop could be on either side, so shrink by one (worst case O(n))."""
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == key:
            return mid
        if a[lo] == a[mid] == a[hi]:
            lo, hi = lo + 1, hi - 1
        elif a[lo] <= a[mid]:
            if a[lo] <= key < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if a[mid] < key <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def staircase_search(grid: list[list], key, trace: list | None = None):
    """Start at the top-right corner; each look removes a row or a column (Figure 3.5)."""
    r, c = 0, len(grid[0]) - 1
    while r < len(grid) and c >= 0:
        v = grid[r][c]
        if trace is not None:
            trace.append((r, c, v))
        if v == key:
            return r, c
        if v > key:
            c -= 1                                # everything below in this column is larger
        else:
            r += 1                                # everything left in this row is smaller
    return None


def first_at_or_after(ring: list, t) -> int | None:
    """Section 3.8: in a rotated sorted log, the index of the first entry >= t (in time order), or None."""
    start = find_rotation(ring)
    n = len(ring)
    lo, hi = 0, n                                 # search positions in time order: index (start + k) % n
    while lo < hi:
        mid = (lo + hi) // 2
        if ring[(start + mid) % n] < t:
            lo = mid + 1
        else:
            hi = mid
    return None if lo == n else (start + lo) % n


if __name__ == "__main__":
    print(find_rotation(ROTATED))
    t = []
    print(search_rotated(ROTATED, 31, t), t)
    t = []
    print(search_rotated(ROTATED, 65, t), t)
    t = []
    print(staircase_search(GRID, 58, t), t)
    t = []
    print(staircase_search(GRID, 50, t), t)
