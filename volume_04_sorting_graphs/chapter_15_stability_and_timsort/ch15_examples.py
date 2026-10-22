"""Volume 4, Chapter 15 - Stability and Timsort: sorting real data, which is rarely random.

A teaching version of Timsort: find natural runs (reversing strictly falling ones) and merge runs from a stack while
keeping run lengths balanced. Python's own sorted() is the full Timsort; the functions min_run, collapse_rule,
timsort_merges, and powersort_merges model its minimum run length and its two merge policies (Section 15.5).

Run:  python3 ch15_examples.py
"""

from __future__ import annotations

import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def find_runs(a: list) -> list[tuple[int, int]]:
    """Cut a into maximal runs, as (start, end) pairs; a strictly falling run is reversed in place (Figure 15.2)."""
    runs, i, n = [], 0, len(a)
    while i < n:
        j = i + 1                                     # the run so far is a[i:j]
        if j < n:
            falling = a[j] < a[i]                     # strictly falling, or rising (equal keys count as rising)
            j += 1
            while j < n and (a[j] < a[j - 1]) == falling:
                j += 1
            if falling:
                a[i:j] = a[i:j][::-1]                 # no equal keys inside, so stability is safe
        runs.append((i, j))
        i = j
    return runs


def merge(a: list, lo: int, mid: int, hi: int) -> None:
    """Stable merge of the sorted runs a[lo:mid] and a[mid:hi], in place."""
    left, right = a[lo:mid], a[mid:hi]
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:                       # ties from the left: stable
            a[k] = left[i]; i += 1
        else:
            a[k] = right[j]; j += 1
        k += 1
    a[k:hi] = left[i:] + right[j:]


class Counted:
    """An item that adds 1 to a shared tally whenever it is compared, so the sorts can stay free of counters."""

    def __init__(self, key, tally: list):
        self.key, self.tally = key, tally

    def __lt__(self, other):
        self.tally[0] += 1
        return self.key < other.key

    def __le__(self, other):
        self.tally[0] += 1
        return self.key <= other.key

    def __ge__(self, other):
        self.tally[0] += 1
        return self.key >= other.key

    def __gt__(self, other):
        self.tally[0] += 1
        return self.key > other.key


def count_comparisons(sort, a: list) -> tuple[list, int]:
    """Run an in-place sort on a copy of a; return (the sorted values, the comparisons it made)."""
    tally = [0]
    b = [Counted(x, tally) for x in a]
    sort(b)
    return [x.key for x in b], tally[0]


def timsort(a: list, counter: dict | None = None, log: list | None = None) -> None:
    """Sort a in place by merging natural runs, smaller neighbours first (the teaching version of Section 15.5).
    counter: if given, counter["comparisons"] grows by the comparisons made; log: the runs and every merge."""
    if counter is not None:                           # count by wrapping the items; the sort itself stays clean
        inner = [] if log is not None else None
        values, comps = count_comparisons(lambda b: timsort(b, log=inner), a)
        a[:] = values
        counter["comparisons"] = counter.get("comparisons", 0) + comps
        if log is not None:
            plain = lambda part: [plain(x) if isinstance(x, list) else x.key for x in part]
            log += [(kind, plain(part)) for kind, part in inner]
        return
    runs = find_runs(a)
    if log is not None:
        log.append(("runs", [a[s:e] for s, e in runs]))
    stack: list[tuple[int, int]] = []
    for run in runs:
        stack.append(run)
        while len(stack) >= 2 and (stack[-2][1] - stack[-2][0]) <= (stack[-1][1] - stack[-1][0]):
            (s1, e1), (s2, e2) = stack[-2], stack.pop()
            merge(a, s1, e1, e2)
            stack[-1] = (s1, e2)
            if log is not None:
                log.append(("merge", a[s1:e2]))
    while len(stack) >= 2:
        (s1, e1), (s2, e2) = stack[-2], stack.pop()
        merge(a, s1, e1, e2)
        stack[-1] = (s1, e2)
        if log is not None:
            log.append(("merge", a[s1:e2]))


def min_run(n: int) -> int:
    """CPython's minimum run length (Section 15.5): n itself below 64; otherwise a number from 32 to 64 chosen so
    that n / min_run is a power of two or a little below one. Take the top six bits of n, and add 1 if any of the
    remaining bits is set."""
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


def collapse_rule(lengths: list[int], log: list | None = None) -> list[int]:
    """Timsort's merge rule on a stack of run lengths (bottom first), as in CPython 3.4-3.10 after the 2015 fix.
    With the top runs ... W, Z, Y, X (X on top) it keeps two invariants: Z > Y + X and Y > X (and, the fix, W > Z + Y).
    While one fails, it merges Y with the smaller of its neighbours. Returns the stack after the new run is in place."""
    p = list(lengths)
    while len(p) > 1:
        n = len(p) - 2                                   # p[n] is Y, p[n + 1] is X
        if (n > 0 and p[n - 1] <= p[n] + p[n + 1]) or (n > 1 and p[n - 2] <= p[n - 1] + p[n]):
            if p[n - 1] < p[n + 1]:
                n -= 1                                   # merge Z and Y instead of Y and X
        elif p[n] > p[n + 1]:
            break                                        # both invariants hold
        if log is not None:
            log.append((p[n], p[n + 1]))
        p[n:n + 2] = [p[n] + p[n + 1]]
    return p


def timsort_merges(run_lengths: list[int]) -> list[tuple[int, int]]:
    """The merges real Timsort (CPython 3.4-3.10) makes for runs of these lengths, in order, as (left, right) sizes."""
    log: list = []
    stack: list[int] = []
    for r in run_lengths:
        stack = collapse_rule(stack + [r], log)
    while len(stack) > 1:                               # merge whatever is left, top first
        log.append((stack[-2], stack[-1]))
        stack[-2:] = [stack[-2] + stack[-1]]
    return log


def power(s1: int, n1: int, n2: int, n: int) -> int:
    """Powersort's 'power' of the boundary between a run [s1, s1 + n1) and the next run of length n2, in a list of
    n items: the depth in the halving tree of [0, n) at which the two runs' midpoints first fall on different sides
    (CPython 3.11+, powerloop in listobject.c)."""
    a, b = 2 * s1 + n1, 2 * s1 + 2 * n1 + n2       # twice the two midpoints
    result = 0
    while True:
        result += 1
        if a >= n:
            a, b = a - n, b - n
        elif b >= n:
            return result
        a, b = 2 * a, 2 * b


def powersort_merges(run_lengths: list[int]) -> list[tuple[int, int]]:
    """The merges Powersort (CPython 3.11+) makes for runs of these lengths: when a new run arrives, merge the top of
    the stack while the boundary below it has a larger power than the new boundary."""
    n = sum(run_lengths)
    log: list = []
    stack: list[list[int]] = []                         # [start, length, power of the boundary above this run]
    start = 0
    for length in run_lengths:
        if stack:
            s1, n1, _ = stack[-1]
            pw = power(s1, n1, length, n)
            while len(stack) > 1 and stack[-2][2] > pw:
                (sa, na, pa), (sb, nb, _) = stack[-2], stack.pop()
                log.append((na, nb))
                stack[-1] = [sa, na + nb, pa]
            stack[-1][2] = pw
        stack.append([start, length, 0])
        start += length
    while len(stack) > 1:
        (sa, na, pa), (sb, nb, _) = stack[-2], stack.pop()
        log.append((na, nb))
        stack[-1] = [sa, na + nb, pa]
    return log


def merge_cost(merges: list[tuple[int, int]]) -> int:
    """Items copied by a list of merges: each merge of sizes a and b copies a + b items."""
    return sum(a + b for a, b in merges)


def merge_sort(a: list, lo: int = 0, hi: int | None = None) -> None:
    """Top-down merge sort of a[lo:hi] in place, with the same stable merge."""
    hi = len(a) if hi is None else hi
    if hi - lo > 1:
        mid = (lo + hi) // 2
        merge_sort(a, lo, mid)
        merge_sort(a, mid, hi)
        merge(a, lo, mid, hi)


def merge_sort_comparisons(a: list) -> int:
    return count_comparisons(merge_sort, a)[1]


def builtin_timing(n: int = 1_000_000, seed: int = 1) -> dict:
    rng = random.Random(seed)
    base = [rng.random() for _ in range(n)]
    nearly = sorted(base)
    for _ in range(n // 1000):
        i, j = rng.randrange(n), rng.randrange(n)
        nearly[i], nearly[j] = nearly[j], nearly[i]
    runs = []
    for k in range(10):
        runs += sorted(base[k * n // 10:(k + 1) * n // 10])
    out = {}
    for name, data in (("random", base), ("sorted", sorted(base)), ("reversed", sorted(base, reverse=True)),
                       ("nearly sorted (0.1% swapped)", nearly), ("ten sorted runs", runs)):
        t = time.perf_counter()
        sorted(data)
        out[name] = round((time.perf_counter() - t) * 1e3, 1)
    return out


if __name__ == "__main__":
    a, c, log = list(PILE), {"comparisons": 0}, []
    timsort(a, c, log)
    print(a, c, log)
    for name, data in (("sorted", list(range(1, 17))), ("reversed", list(range(16, 0, -1))),
                       ("two runs", [3, 8, 12, 15, 21, 27, 30, 34, 2, 5, 9, 14, 18, 22, 25, 33])):
        c = {"comparisons": 0}
        b = list(data)
        timsort(b, c)
        print(name, c, merge_sort_comparisons(data), b == sorted(data))
    print([min_run(n) for n in (0, 1, 63, 64, 65, 100, 1000, 2112, 1_000_000)])
    print(collapse_rule([120, 80, 25], []), collapse_rule([120, 80, 25, 20], []))
    runs = [1000, 1, 1, 1, 1, 1, 1, 1]
    print(timsort_merges(runs), merge_cost(timsort_merges(runs)), powersort_merges(runs), merge_cost(powersort_merges(runs)))
    left_to_right = [(1000 + i, 1) for i in range(7)]
    print(merge_cost(left_to_right))
    print(builtin_timing())
