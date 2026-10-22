"""Volume 6, Chapter 6 - model solutions to the Thinking Problems (Section 6.14)."""

from __future__ import annotations

from ch06_examples import fractional_bound

VOUCHERS = [3, 34, 4, 12, 5, 2, 17, 9, 21, 8]       # Chapter 5's wallet


def fewest_vouchers(values: list, target: int) -> tuple[list | None, int]:
    """Pay target exactly with as few vouchers as possible, by depth-first branch and bound.
    Vouchers are tried largest first; a branch needing `need` more pounds needs at least
    ceil(need / largest undecided voucher) more vouchers, so it is cut when that cannot beat the best.
    Returns (vouchers or None, nodes visited)."""
    vals = sorted(values, reverse=True)
    suffix = [0] * (len(vals) + 1)
    for i in range(len(vals) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + vals[i]
    best, nodes = [None], [0]

    def go(i, need, chosen):
        nodes[0] += 1
        if need == 0:
            if best[0] is None or len(chosen) < len(best[0]):
                best[0] = list(chosen)
            return
        if i == len(vals) or need < 0 or suffix[i] < need:
            return                                    # overshoot or unreachable (Chapter 5)
        bound = len(chosen) + -(-need // vals[i])     # at least this many vouchers in all
        if best[0] is not None and bound >= len(best[0]):
            return                                    # cannot use fewer than the best: cut
        chosen.append(vals[i])
        go(i + 1, need - vals[i], chosen)
        chosen.pop()
        go(i + 1, need, chosen)

    go(0, target, [])
    return best[0], nodes[0]


def unsorted_branch_and_bound(books: list, budget: int) -> int:
    """Thinking Problem 3's bug: the books are never sorted by votes per pound, so the 'fractional bound'
    fills in list order and can fall below the truth. Returns the votes it reports."""
    best = [0]

    def go(i, room, votes):
        best[0] = max(best[0], votes)
        if i == len(books) or votes + fractional_bound(books, i, room) <= best[0]:
            return
        _, price, v = books[i]
        if price <= room:
            go(i + 1, room - price, votes + v)
        go(i + 1, room, votes)

    go(0, budget, 0)
    return best[0]
