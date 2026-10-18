"""Volume 11, Chapter 9 - The Big Comparison: Backtracking vs. Divide-and-Conquer vs. Brute Force.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import itertools
import timeit


def subset_sum_brute(values: list[int], target: int) -> tuple[bool, int]:
    """Brute force: build every complete subset, then check. Returns (found, candidates examined)."""
    examined = 0
    for r in range(len(values) + 1):
        for combo in itertools.combinations(values, r):
            examined += 1
            if sum(combo) == target:
                return True, examined
    return False, examined


def subset_sum_backtrack(values: list[int], target: int) -> tuple[bool, int]:
    """Backtracking with pruning: largest first, stop on overshoot or when the rest can't reach the target."""
    vals = sorted(values, reverse=True)
    suffix = [0] * (len(vals) + 1)
    for i in range(len(vals) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + vals[i]
    nodes = 0

    def go(i: int, total: int) -> bool:
        nonlocal nodes
        nodes += 1
        if total == target:
            return True
        if i == len(vals) or total > target or total + suffix[i] < target:
            return False
        return go(i + 1, total + vals[i]) or go(i + 1, total)

    return go(0, 0), nodes


def subset_sum_meet_in_middle(values: list[int], target: int) -> bool:
    """Divide-and-conquer flavour: split the list in half, list every subset sum of each half (2^(n/2) each),
    then look for a pair adding to the target. O(2^(n/2) n) instead of O(2^n)."""
    half = len(values) // 2

    def sums(part: list[int]) -> set[int]:
        out = {0}
        for v in part:
            out |= {s + v for s in out}
        return out

    left, right = sums(values[:half]), sums(values[half:])
    return any(target - s in right for s in left)


def race(values: list[int], target: int) -> dict[str, float]:
    return {
        "brute force": min(timeit.repeat(lambda: subset_sum_brute(values, target), number=1, repeat=3)),
        "backtracking": min(timeit.repeat(lambda: subset_sum_backtrack(values, target), number=1, repeat=3)),
        "meet in the middle": min(timeit.repeat(lambda: subset_sum_meet_in_middle(values, target), number=1, repeat=3)),
    }


def choose_search(features: set[str]) -> str:
    """Decision guide for search problems."""
    if "need the best value, with a good optimistic bound" in features:
        return "branch-and-bound"
    if "rules can be checked on partial solutions" in features:
        return "backtracking"
    if "splits into independent halves to combine" in features:
        return "divide and conquer (e.g. meet in the middle)"
    if "subproblems repeat" in features:
        return "dynamic programming (Volume 12)"
    if "tiny input" in features:
        return "brute force"
    return "brute force baseline, then look for structure"


if __name__ == "__main__":
    vals = [62, 94, 36, 104, 52, 78, 28, 122, 46, 90, 74, 58, 110, 24, 82, 66, 40, 116]   # all even
    target = 641                                        # odd, so impossible - but no simple bound notices
    print("brute:", subset_sum_brute(vals, target), "| backtracking:", subset_sum_backtrack(vals, target),
          "| meet in the middle:", subset_sum_meet_in_middle(vals, target))
    print({k: f"{v * 1000:.2f} ms" for k, v in race(vals, target).items()})
    print(choose_search({"rules can be checked on partial solutions"}))
