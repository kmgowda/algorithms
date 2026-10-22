"""Volume 4, Chapter 7 - Quicksort in Practice: model solutions to the Thinking Problems (Section 7.16).

Run:  python3 ch07_solutions.py
"""

from __future__ import annotations

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def dual_pivot_partition(a: list, lo: int, hi: int, counter: dict | None = None) -> tuple[int, int]:
    """Thinking Problem 2: one pass with two pivots p = a[lo] <= q = a[hi]. Afterwards a[lo..l-1] < p = a[l],
    p <= a[l+1..g-1] <= q = a[g], and a[g+1..hi] > q. Returns (l, g), the pivots' final places."""
    def less(x, y):
        if counter is not None:
            counter["comparisons"] += 1
        return x < y
    if less(a[hi], a[lo]):
        a[lo], a[hi] = a[hi], a[lo]
    p, q = a[lo], a[hi]
    lt, i, gt = lo + 1, lo + 1, hi - 1
    while i <= gt:
        if less(a[i], p):                         # below both pivots: grow the left part
            a[i], a[lt] = a[lt], a[i]
            lt += 1
            i += 1
        elif less(q, a[i]):                       # above both pivots: swap to the right part, look again at i
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:                                     # between the pivots: leave it in the middle
            i += 1
    lt, gt = lt - 1, gt + 1
    a[lo], a[lt] = a[lt], a[lo]
    a[hi], a[gt] = a[gt], a[hi]
    return lt, gt


def dual_pivot_quicksort(a: list, lo: int = 0, hi: int | None = None, counter: dict | None = None) -> None:
    """Sort a[lo..hi] in place: partition around two pivots, then sort the three parts."""
    if hi is None:
        hi = len(a) - 1
    if lo >= hi:
        return
    l, g = dual_pivot_partition(a, lo, hi, counter)
    dual_pivot_quicksort(a, lo, l - 1, counter)
    if a[l] < a[g]:                               # equal pivots: the middle part is all copies of them
        dual_pivot_quicksort(a, l + 1, g - 1, counter)
    dual_pivot_quicksort(a, g + 1, hi, counter)


def partition3_buggy(a: list, lo: int, hi: int, pivot) -> tuple[int, int]:
    """Thinking Problem 3: the three-way partition with one slip, i advances after a swap from the back."""
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
            i += 1                                # the bug: the item just swapped in is never examined
        else:
            i += 1
    return lt, gt


def hoare_returns(a: list, lo: int, hi: int, middle: bool = True) -> int:
    """Thinking Problem 1: the split point of Hoare's partition with the pivot taken from the middle (as in the
    chapter) or, if middle is False, from the last position."""
    pivot = a[(lo + hi) // 2] if middle else a[hi]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < pivot:
            i += 1
        j -= 1
        while a[j] > pivot:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]


if __name__ == "__main__":
    a = list(PILE)
    c = {"comparisons": 0}
    print(dual_pivot_partition(a, 0, 8, c), a, c)
    b = [2, 3, 1]
    print(partition3_buggy(b, 0, 2, 2), b)
    print(hoare_returns([12, 25], 0, 1, middle=False), hoare_returns([12, 25], 0, 1))
