"""Volume 4, Chapter 12 - Thinking Problems (Section 12.16): model solutions that can be run.

1. fibonacci_stack_bound: the most runs a stack obeying Z > Y + X and Y > X can hold for n items.
2. natural_merge_sort: merge the natural runs in rounds of neighbouring pairs: O(n + n log r) comparisons.
3. teaching_merges and staircase: the teaching rule of Section 12.5 copies Theta(n^1.5) items on runs k, k-1, ..., 1.

Run:  python3 ch12_solutions.py
"""

from __future__ import annotations

from ch12_examples import count_comparisons, find_runs, merge, merge_cost, merge_sort, timsort, timsort_merges


# ---------------------------------------------------------------- Thinking Problem 1

def fibonacci_stack_bound(n: int) -> int:
    """The most runs a stack can hold when its lengths, read from the top, satisfy r1 >= 1, r2 > r1 and
    r(i+2) > r(i+1) + r(i), and they add up to at most n. The shortest such stack has r1 = 1, r2 = 2, r(i+2) = r(i+1) + r(i) + 1."""
    count, total, a, b = 0, 0, 1, 2
    while total + a <= n:
        total += a
        count += 1
        a, b = b, a + b + 1
    return count


# ---------------------------------------------------------------- Thinking Problem 2

def natural_merge_sort(a: list) -> None:
    """Sort a in place: find the natural runs, then merge neighbouring pairs of runs, round after round,
    until one run is left. Stable; at most (n - 1) + n * ceil(log2 r) comparisons for r runs."""
    runs = find_runs(a)
    while len(runs) > 1:
        merged = []
        for k in range(0, len(runs) - 1, 2):
            (lo, mid), (_, hi) = runs[k], runs[k + 1]
            merge(a, lo, mid, hi)
            merged.append((lo, hi))
        if len(runs) % 2:
            merged.append(runs[-1])                    # an odd run out waits for the next round
        runs = merged


def natural_bound(n: int, r: int) -> int:
    """The guarantee of the model solution: (n - 1) for the scan plus n per round, ceil(log2 r) rounds."""
    return max(0, n - 1) + n * (r - 1).bit_length() if r > 0 else 0


# ---------------------------------------------------------------- Thinking Problem 3

def teaching_merges(run_lengths: list[int]) -> list[tuple[int, int]]:
    """The merges the teaching Timsort of Section 12.5 makes, as (left, right) sizes: after each push, merge the
    top two while the second is no longer than the top; at the end merge what is left, top first."""
    log, stack = [], []
    for r in run_lengths:
        stack.append(r)
        while len(stack) >= 2 and stack[-2] <= stack[-1]:
            log.append((stack[-2], stack[-1]))
            stack[-2:] = [stack[-2] + stack[-1]]
    while len(stack) >= 2:
        log.append((stack[-2], stack[-1]))
        stack[-2:] = [stack[-2] + stack[-1]]
    return log


def staircase(k: int) -> list[int]:
    """A list of n = k(k + 1)/2 distinct items whose natural runs have lengths k, k - 1, ..., 1: deal the values
    0, 1, 2, ... in turn to the runs that still have room, so every run rises and the runs interleave."""
    lengths = list(range(k, 0, -1))
    runs = [[] for _ in lengths]
    value, open_runs = 0, list(range(k))
    while open_runs:
        for t in list(open_runs):
            runs[t].append(value)
            value += 1
            if len(runs[t]) == lengths[t]:
                open_runs.remove(t)
    return [v for run in runs for v in run]


def staircase_costs(k: int) -> dict:
    """Items copied by each merge policy, and comparisons made, on the staircase of k runs."""
    a = staircase(k)
    lengths = [e - s for s, e in find_runs(list(a))]
    return {"n": len(a), "runs": lengths == list(range(k, 0, -1)),
            "teaching copies": merge_cost(teaching_merges(lengths)),
            "Timsort copies": merge_cost(timsort_merges(lengths)),
            "teaching comparisons": count_comparisons(timsort, a)[1],
            "merge sort comparisons": count_comparisons(merge_sort, a)[1],
            "natural comparisons": count_comparisons(natural_merge_sort, a)[1]}


if __name__ == "__main__":
    print([fibonacci_stack_bound(n) for n in (0, 1, 3, 6, 11, 1000, 1_000_000)])
    for k in (4, 10, 20, 40, 80, 160):
        print(k, staircase_costs(k))
    print(staircase(4))
