"""Volume 3, Chapter 18 - Fenwick Trees: companion code for the Thinking Problems (Section 18.16).

Run:  python3 ch18_solutions.py
"""

from __future__ import annotations

from ch18_examples import Fenwick, lowbit


def stretch(i: int) -> range:
    """The days box i covers: the lowbit(i) days ending at day i (Thinking Problem 1)."""
    return range(i - lowbit(i) + 1, i + 1)


def first_reaching(f: Fenwick, s: int):
    """Thinking Problem 2: the first day whose prefix total reaches s (s >= 1, every count >= 0), in O(log n).
    Walk down from the largest power of two, taking a box whenever the total stays below s."""
    if s < 1:
        raise ValueError("s must be at least 1")
    pos, step = 0, 1 << max(0, f.n.bit_length() - 1)
    while step:
        if pos + step <= f.n and f.tree[pos + step] < s:
            pos += step
            s -= f.tree[pos]
        step //= 2
    return pos + 1 if pos < f.n else None


def kth_lowest_score(scores: list[int], k: int, top: int = 100):
    """The k-th lowest score so far, from a score-indexed Fenwick tree of counts (Section 18.8)."""
    f = Fenwick([0] * top)
    for x in scores:
        f.add(x, 1)
    return first_reaching(f, k)


def build_right_to_left(values: list[int]) -> list[int]:
    """Thinking Problem 3: the flawed build that hands totals up from the LAST box to the first."""
    n = len(values)
    tree = [0] + list(values)
    for i in range(n, 0, -1):
        j = i + lowbit(i)
        if j <= n:
            tree[j] += tree[i]
    return tree[1:]


if __name__ == "__main__":
    print([list(stretch(i)) for i in (6, 8, 12)])
    f = Fenwick([3, 1, 4, 1, 5, 9, 2, 6])
    print(first_reaching(f, 15), first_reaching(f, 31), first_reaching(f, 32))
    print(kth_lowest_score([72, 95, 41, 88, 60], 2))
    print(build_right_to_left([3, 1, 4, 1, 5, 9, 2, 6]))
