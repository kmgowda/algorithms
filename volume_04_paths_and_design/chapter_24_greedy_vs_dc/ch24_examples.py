"""Volume 4, Chapter 24 - Greedy versus Divide and Conquer: the same problems, two ways of thinking.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

VISITORS = [12, 7, 21, 15, 3, 18, 9, 26]


def max_greedy(values: list, counter: list) -> int:
    """Scan once, keeping the best so far: n - 1 comparisons."""
    best = values[0]
    for v in values[1:]:
        counter[0] += 1
        best = max(best, v)
    return best


def max_dc(values: list, counter: list) -> int:
    """Split, find each half's maximum, compare once: also n - 1 comparisons, but the halves are independent."""
    if len(values) == 1:
        return values[0]
    mid = len(values) // 2
    a, b = max_dc(values[:mid], counter), max_dc(values[mid:], counter)
    counter[0] += 1
    return max(a, b)


def depth(n: int) -> int:
    """Rounds needed if every comparison in a round can happen at once (Figure 24.2)."""
    return 0 if n <= 1 else 1 + depth((n + 1) // 2)


def sort_greedy(values: list, counter: list) -> list:
    """Selection sort: greedily take the smallest remaining item each time."""
    left, out = list(values), []
    while left:
        i = 0
        for j in range(1, len(left)):
            counter[0] += 1
            if left[j] < left[i]:
                i = j
        out.append(left.pop(i))
    return out


def sort_dc(values: list, counter: list) -> list:
    """Merge sort: split, sort the halves, merge."""
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    a, b = sort_dc(values[:mid], counter), sort_dc(values[mid:], counter)
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        counter[0] += 1
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return out + a[i:] + b[j:]


if __name__ == "__main__":
    a, b = [0], [0]
    print(max_greedy(VISITORS, a), a[0], max_dc(VISITORS, b), b[0], depth(8))
    for n in (8, 100, 1000):
        import random
        v = random.Random(n).sample(range(10 * n), n)
        c, d = [0], [0]
        sort_greedy(v, c); sort_dc(v, d)
        print(n, c[0], d[0], depth(n))
