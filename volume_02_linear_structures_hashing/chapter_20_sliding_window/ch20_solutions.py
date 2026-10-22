"""Volume 2, Chapter 20 - Thinking Problem solutions (Section 20.16)."""

from __future__ import annotations


def shortest_covering(log: str) -> tuple[int, int]:
    """Thinking Problem 20.2: (length, start) of the shortest stretch holding every reader of the log.

    O(n) time; the map holds one count per reader. Returns (0, 0) for an empty log."""
    need = len(set(log))
    inside: dict[str, int] = {}
    left, best = 0, (0, 0)
    for right, r in enumerate(log):
        inside[r] = inside.get(r, 0) + 1                  # grow on the right
        while inside[log[left]] > 1:                       # the leftmost reader appears again later
            inside[log[left]] -= 1
            left += 1
        if len(inside) == need and (best[0] == 0 or right - left + 1 < best[0]):
            best = (right - left + 1, left)
    return best


def shortest_stretch_if(counts: list[int], target: int) -> int:
    """Thinking Problem 20.3: the buggy version that shrinks at most once per new day."""
    left, total, best = 0, 0, 0
    for right, c in enumerate(counts):
        total += c
        if left < right and total - counts[left] >= target:    # 'if' where 'while' is needed
            total -= counts[left]
            left += 1
        if total >= target and (best == 0 or right - left + 1 < best):
            best = right - left + 1
    return best
