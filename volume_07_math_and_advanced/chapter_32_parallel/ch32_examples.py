"""Volume 7, Chapter 32 - Parallel Algorithms: work, span, and how many helpers really help.

Run:  python3 ch32_examples.py
"""

from __future__ import annotations

import math


def tree_sum(values: list) -> tuple[int, int, int]:
    """Add pairs in rounds, all pairs of a round at once (Figure 32.1). Returns (total, additions = work, rounds = span)."""
    level, work, rounds = list(values), 0, 0
    if not level:
        return 0, 0, 0
    while len(level) > 1:
        nxt = [level[i] + level[i + 1] for i in range(0, len(level) - 1, 2)]
        work += len(nxt)
        if len(level) % 2:
            nxt.append(level[-1])
        level, rounds = nxt, rounds + 1
    return level[0], work, rounds


def prefix_sums_parallel(values: list) -> tuple[list, int, int]:
    """Hillis-Steele scan (Figure 32.4): in round r, every position adds the value 2^r places to its left.
    Returns (running totals, additions, rounds)."""
    a, work, rounds, step = list(values), 0, 0, 1
    while step < len(a):
        a = [a[i] + (a[i - step] if i >= step else 0) for i in range(len(a))]
        work += len(a) - step
        rounds += 1
        step *= 2
    return a, work, rounds


def time_with_helpers(work: int, span: int, helpers: int) -> float:
    """Brent's bound: about work / helpers + span steps."""
    return work / helpers + span


def amdahl(parallel_share: float, helpers: int) -> float:
    """Speed-up when only part of a job can be shared out (Figure 32.7)."""
    return 1 / ((1 - parallel_share) + parallel_share / helpers)


# ---------------------------------------------------------------- the fork-join model, as a DAG of unit steps

def tree_sum_dag(n: int) -> dict:
    """The computation DAG of a fork-join tree sum of n values (Figure 32.2): node -> list of nodes it must wait for.
    Leaves are the values (one read step each); every inner node is one addition."""
    deps, counter = {}, [0]

    def build(lo, hi):
        counter[0] += 1
        node = counter[0]
        if hi - lo == 1:
            deps[node] = []
        else:
            mid = (lo + hi) // 2
            deps[node] = [build(lo, mid), build(mid, hi)]
        return node
    if n:
        build(0, n)
    return deps


def work_span(deps: dict) -> tuple[int, int]:
    """Work = number of unit steps; span = the longest chain of steps that must run one after another."""
    memo = {}

    def depth(v):
        if v not in memo:
            memo[v] = 1 + max((depth(u) for u in deps[v]), default=0)
        return memo[v]
    return len(deps), max((depth(v) for v in deps), default=0)


def greedy_schedule(deps: dict, p: int) -> int:
    """A greedy scheduler: at every step, run up to p steps whose inputs are ready. Returns the number of steps taken.
    Brent: never more than work / p + span."""
    done, t = set(), 0
    remaining = set(deps)
    while remaining:
        ready = sorted(v for v in remaining if all(u in done for u in deps[v]))
        run = ready[:p]
        for v in run:
            done.add(v)
            remaining.discard(v)
        t += 1
    return t


# ---------------------------------------------------------------- a race on a shared counter

def race_outcomes(increments_per_helper: int = 1, helpers: int = 2) -> dict:
    """Every interleaving of 'read counter, then write counter + 1' by several helpers on a shared counter that starts
    at 0: how often each final value occurs (Figure 32.3)."""
    from collections import Counter
    import itertools
    steps = [(h, k, part) for h in range(helpers) for k in range(increments_per_helper) for part in ("read", "write")]
    outcomes = Counter()
    labels = []
    for h in range(helpers):
        labels += [h] * (2 * increments_per_helper)
    seen = set()
    for order in itertools.permutations(range(len(labels))):
        seq = tuple(labels[i] for i in order)
        if seq in seen:
            continue
        seen.add(seq)
        counter, local, pos = 0, [0] * helpers, [0] * helpers
        for h in seq:
            if pos[h] % 2 == 0:
                local[h] = counter
            else:
                counter = local[h] + 1
            pos[h] += 1
        outcomes[counter] += 1
    return dict(outcomes)


# ---------------------------------------------------------------- Blelloch's work-efficient scan

def blelloch_scan(values: list) -> tuple[list, int, int, list]:
    """Exclusive prefix sums in two sweeps over a balanced tree (Figure 32.5). Length padded to a power of two.
    Returns (exclusive sums, additions, rounds, array after the up-sweep)."""
    if not values:
        return [], 0, 0, []
    n = 1
    while n < len(values):
        n *= 2
    a = list(values) + [0] * (n - len(values))
    work = rounds = 0
    d = 1
    while d < n:                                          # up-sweep: partial sums of blocks
        for i in range(2 * d - 1, n, 2 * d):
            a[i] += a[i - d]
            work += 1
        d *= 2
        rounds += 1
    after_up = list(a)
    if n:
        a[n - 1] = 0
    d = n // 2
    while d >= 1:                                         # down-sweep: pass totals of left siblings to the right
        for i in range(2 * d - 1, n, 2 * d):
            left = a[i - d]
            a[i - d] = a[i]
            a[i] += left
            work += 1
        d //= 2
        rounds += 1
    return a[:len(values)], work, rounds, after_up


# ---------------------------------------------------------------- parallel merge sort: span recurrences

def merge_spans(n: int) -> dict:
    """Spans (in unit steps) of merge sort of n items with a serial merge and with a parallel merge.
    Serial merge: S(n) = S(n/2) + n. Parallel merge by binary-search splitting: M(n) = M(3n/4) + log2 n (rounded down), and
    S(n) = S(n/2) + M(n), about log^3 n. Work stays about n log2 n."""
    import functools

    @functools.lru_cache(maxsize=None)
    def pmerge(m):
        return 1 if m <= 1 else math.ceil(math.log2(m)) + pmerge(3 * m // 4)

    @functools.lru_cache(maxsize=None)
    def span_serial(m):
        return 1 if m <= 1 else span_serial(m // 2) + m

    @functools.lru_cache(maxsize=None)
    def span_parallel(m):
        return 1 if m <= 1 else span_parallel(m // 2) + pmerge(m)
    work = round(n * math.log2(n)) if n > 1 else 1
    return {"work": work, "span serial merge": span_serial(n), "span parallel merge": span_parallel(n),
            "parallelism serial": round(work / span_serial(n), 1), "parallelism parallel": round(work / span_parallel(n))}


def parallel_merge(a: list, b: list) -> list:
    """The parallel merge's idea, run sequentially: take the middle of the longer list, find its place in the other by
    binary search, and merge the two halves on each side independently (they could run at the same time)."""
    import bisect
    if len(a) < len(b):
        a, b = b, a
    if not a:
        return []
    mid = len(a) // 2
    j = bisect.bisect_left(b, a[mid])
    return parallel_merge(a[:mid], b[:j]) + [a[mid]] + parallel_merge(a[mid + 1:], b[j:])


if __name__ == "__main__":
    print(tree_sum(list(range(1, 17))), tree_sum(list(range(1, 1025)))[1:])
    print(prefix_sums_parallel([3, 1, 4, 1, 5, 9, 2, 6]))
    w, s = 1023, 10
    print([round(time_with_helpers(w, s, p), 1) for p in (1, 4, 32, 1024)])
    print([round(amdahl(0.9, p), 2) for p in (2, 8, 64, 1000)])
    dag = tree_sum_dag(16)
    W, S = work_span(dag)
    print(W, S, [(p, greedy_schedule(dag, p), round(W / p + S, 1), max(math.ceil(W / p), S)) for p in (1, 2, 4, 8, 16)])
    print(race_outcomes(1, 2), race_outcomes(2, 2))
    print(blelloch_scan([3, 1, 4, 1, 5, 9, 2, 6]))
    print(merge_spans(1_000_000), merge_spans(1024))
    print(parallel_merge([1, 4, 9, 12], [2, 3, 10, 15, 20]))
