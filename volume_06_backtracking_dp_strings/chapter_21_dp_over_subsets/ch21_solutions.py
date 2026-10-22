"""Volume 6, Chapter 21 - model solutions to the Thinking Problems (Section 21.14)."""

from __future__ import annotations


def fewest_cover(k: int, skills: list) -> tuple[float, list]:
    """Thinking Problem 2: the fewest volunteers whose skills (bit masks over k skills) together cover all k.
    fewest[mask] = fewest volunteers whose skills together are exactly mask; masks only grow, so increasing
    numeric order is a safe fill order. O(2^k x p). Returns (count, chosen volunteers), or (inf, []) if impossible."""
    full = (1 << k) - 1
    inf = float("inf")
    fewest, came = [inf] * (full + 1), [None] * (full + 1)
    fewest[0] = 0
    for mask in range(full + 1):
        if fewest[mask] == inf:
            continue
        for v, s in enumerate(skills):
            new = mask | s
            if fewest[mask] + 1 < fewest[new]:
                fewest[new], came[new] = fewest[mask] + 1, (mask, v)
    if fewest[full] == inf:
        return inf, []
    chosen, mask = [], full
    while mask and came[mask] is not None:
        mask, v = came[mask]
        chosen.append(v)
    return fewest[full], sorted(chosen)


def set_only_round(d: list) -> int:
    """Thinking Problem 3's bug: keep only the shortest route to each SET (forgetting where it ends), and
    extend that one route. Wrong: the van's map gives 23 instead of 21."""
    n = len(d)
    if n == 1:
        return 0
    best = {0: (0, 0)}                                 # mask -> (length, last place)
    full = (1 << n) - 2
    for mask in range(0, full + 1, 2):
        if mask not in best:
            continue
        length, last = best[mask]
        for j in range(1, n):
            if not mask & (1 << j):
                cand = (length + d[last][j], j)
                new = mask | (1 << j)
                if new not in best or cand < best[new]:
                    best[new] = cand
    length, last = best[full]
    return length + d[last][0]


if __name__ == "__main__":
    from ch21_examples import BRANCHES, TRAVEL, held_karp, matrix
    print(fewest_cover(5, [0b00011, 0b01100, 0b10001, 0b10110, 0b01000]))
    d = matrix(BRANCHES, TRAVEL)
    print(set_only_round(d), held_karp(d)[0])
