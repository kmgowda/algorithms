"""Volume 6, Chapter 5 - model solutions to the Thinking Problems (Section 5.14)."""

from __future__ import annotations

from ch05_examples import subset_sum


def equal_split(values: list) -> tuple[list | None, int]:
    """Split the vouchers into two piles of equal value. An odd total is refused at once; otherwise the biggest
    voucher is put in pile 1 (the piles are interchangeable) and the pruned subset-sum search looks for the
    rest of half the total among the others. Returns (pile 1 or None, nodes visited)."""
    total = sum(values)
    if total % 2:
        return None, 0
    if not values:
        return [], 0
    vals = sorted(values, reverse=True)
    rest, nodes = subset_sum(vals[1:], total // 2 - vals[0], prune=True, sort_first=True)
    if total // 2 - vals[0] < 0 or rest is None:
        return None, nodes
    return [vals[0]] + rest, nodes


def max_reach_bug(values: list, target: int) -> tuple[list | None, int]:
    """Thinking Problem 3's bug: 'can the rest reach it?' tested with the largest undecided voucher
    instead of the sum of all of them."""
    nodes = [0]

    def go(i, total, chosen):
        nodes[0] += 1
        if total == target:
            return list(chosen)
        if i == len(values):
            return None
        if total > target or total + max(values[i:]) < target:
            return None
        chosen.append(values[i])
        found = go(i + 1, total + values[i], chosen)
        chosen.pop()
        return found or go(i + 1, total, chosen)

    return go(0, 0, []), nodes[0]
