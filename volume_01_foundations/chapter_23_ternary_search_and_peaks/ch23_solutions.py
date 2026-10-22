"""Volume 1, Chapter 23, Thinking Problem 2 - finding a visitor count in a day that rises, then falls.

Find the peak by binary search on the slope, then binary search the rising part (sorted upwards) and the falling
part (sorted downwards) separately: O(log n) looks in all.

Run:  python3 ch23_solutions.py
"""

from __future__ import annotations

from ch23_examples import VISITORS, peak_by_slope


def search_rise_and_fall(a: list, key) -> int:
    """Position of key in a list that strictly rises to one peak and then strictly falls, or -1.
    If the key occurs on both sides, the earlier (rising-side) position is returned."""
    if not a:
        return -1
    p = peak_by_slope(a)
    lo, hi = 0, p + 1                             # rising part a[0..p]: lower bound of key
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid
    if lo <= p and a[lo] == key:
        return lo
    lo, hi = p + 1, len(a) - 1                    # falling part a[p+1..n-1], largest first
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == key:
            return mid
        if a[mid] > key:
            lo = mid + 1                          # falling: smaller values lie to the right
        else:
            hi = mid - 1
    return -1


if __name__ == "__main__":
    print(search_rise_and_fall(VISITORS, 50))     # 7: the 16:00 hour
