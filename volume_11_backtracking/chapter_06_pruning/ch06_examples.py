"""Volume 11, Chapter 6 - Pruning: Cutting Branches Early.

Every search here counts the nodes it visits, so the effect of each pruning idea can be measured.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations


def subset_sum_count(values: list[int], target: int, prune: str = "none") -> tuple[bool, int]:
    """Is there a subset adding to target (positive values)? Returns (found, nodes visited).
    prune = 'none'      : explore the full include/exclude tree
            'overshoot' : stop when the running sum exceeds the target
            'bounds'    : also stop when even taking ALL remaining values can't reach the target
            'sorted'    : 'bounds' plus trying the largest values first."""
    vals = sorted(values, reverse=True) if prune == "sorted" else list(values)
    suffix = [0] * (len(vals) + 1)
    for i in range(len(vals) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + vals[i]
    nodes = 0

    def go(i: int, total: int) -> bool:
        nonlocal nodes
        nodes += 1
        if total == target:
            return True
        if i == len(vals):
            return False
        if prune != "none" and total > target:
            return False
        if prune in ("bounds", "sorted") and total + suffix[i] < target:
            return False                                  # can't reach the target any more
        return go(i + 1, total + vals[i]) or go(i + 1, total)

    found = go(0, 0)
    return found, nodes


def can_partition_k(values: list[int], k: int, symmetry: bool = True) -> tuple[bool, int]:
    """LeetCode 698: split values into k groups with equal sums. Returns (possible, nodes).
    Pruning: largest first; skip a value that doesn't fit; with symmetry=True, never put a value into a
    second EMPTY group - all empty groups are interchangeable, so trying more than one is wasted work."""
    total = sum(values)
    if k <= 0 or total % k:
        return False, 0
    goal = total // k
    vals = sorted(values, reverse=True)
    if vals and vals[0] > goal:
        return False, 0
    groups = [0] * k
    nodes = 0

    def go(i: int) -> bool:
        nonlocal nodes
        nodes += 1
        if i == len(vals):
            return all(g == goal for g in groups)
        for g in range(k):
            if groups[g] + vals[i] > goal:
                continue
            groups[g] += vals[i]
            if go(i + 1):
                return True
            groups[g] -= vals[i]
            if symmetry and groups[g] == 0:
                break                                     # the other empty groups would behave identically
        return False

    return go(0), nodes


def queens_nodes(n: int, check_early: bool) -> tuple[int, int]:
    """N-Queens solutions and nodes: checking attacks when placing vs. only at the end."""
    nodes, solutions = 0, 0
    cols: list[int] = []

    def safe(c: int) -> bool:
        r = len(cols)
        return all(c != cc and abs(c - cc) != r - rr for rr, cc in enumerate(cols))

    def go() -> None:
        nonlocal nodes, solutions
        nodes += 1
        if len(cols) == n:
            if check_early or all(cols[i] != cols[j] and abs(cols[i] - cols[j]) != j - i
                                  for i in range(n) for j in range(i + 1, n)):
                solutions += 1
            return
        for c in range(n):
            if check_early and not safe(c):
                continue
            cols.append(c)
            go()
            cols.pop()

    go()
    return solutions, nodes


def delivery_load_balance(parcels: list[int], vans: int) -> tuple[bool, int]:
    """Industry example: can parcels be split so every van carries exactly the same weight?"""
    return can_partition_k(parcels, vans)


if __name__ == "__main__":
    vals = [27, 41, 19, 33, 8, 15, 22, 37, 11, 29, 5, 46, 13, 31, 24, 17]
    for p in ("none", "overshoot", "bounds", "sorted"):
        print(f"subset sum, prune={p:9}:", subset_sum_count(vals, 151, p))
    print("subset sum, impossible target 999:", subset_sum_count(vals, 999, "bounds"))
    parcels = [8, 9, 9, 5, 6, 9, 5, 2, 6, 8, 9, 9]           # 85 kg into 5 vans of 17 kg: impossible
    print("5 vans, symmetry breaking:", can_partition_k(parcels, 5, True),
          "| without:", can_partition_k(parcels, 5, False))
    print("6-queens check early:", queens_nodes(6, True), "| only at the end:", queens_nodes(6, False))
