"""Volume 4, Chapter 8 - Merge Sort: model solutions to the Thinking Problems (Section 8.16).

Run:  python3 ch08_solutions.py
"""

from __future__ import annotations

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def smaller_to_the_right(a: list) -> list:
    """Thinking Problem 2: for every position p, how many later items are strictly smaller than a[p].
    Merge sort on positions; when an item leaves the left half, every right item already taken is smaller."""
    counts = [0] * len(a)

    def sort(pos: list) -> list:
        if len(pos) <= 1:
            return pos
        mid = len(pos) // 2
        left, right = sort(pos[:mid]), sort(pos[mid:])
        out, i, j = [], 0, 0
        while i < len(left) or j < len(right):
            if j == len(right) or (i < len(left) and a[left[i]] <= a[right[j]]):
                counts[left[i]] += j               # the j right items taken so far are all smaller
                out.append(left[i]); i += 1
            else:
                out.append(right[j]); j += 1
        return out

    sort(list(range(len(a))))
    return counts


def bottom_up_buggy(a: list) -> list:
    """Thinking Problem 3: the plausible but wrong bottom-up merge sort (merges only complete pairs of runs)."""
    a, n, width = list(a), len(a), 1
    while width < n:
        for lo in range(0, n - 2 * width + 1, 2 * width):
            mid, hi = lo + width, lo + 2 * width
            a[lo:hi] = _merge(a[lo:mid], a[mid:hi])
        width *= 2
    return a


def bottom_up(a: list) -> list:
    """The repaired version: also merge a final, shorter right run (stop only when no right run exists)."""
    a, n, width = list(a), len(a), 1
    while width < n:
        lo = 0
        while lo + width < n:
            mid, hi = lo + width, min(lo + 2 * width, n)
            a[lo:hi] = _merge(a[lo:mid], a[mid:hi])
            lo += 2 * width
        width *= 2
    return a


def _merge(left: list, right: list) -> list:
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


if __name__ == "__main__":
    print(smaller_to_the_right(PILE), sum(smaller_to_the_right(PILE)))
    print(bottom_up_buggy(PILE), bottom_up(PILE))
