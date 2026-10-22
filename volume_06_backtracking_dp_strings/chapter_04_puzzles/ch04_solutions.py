"""Volume 6, Chapter 4 - model solutions to the Thinking Problems (Section 4.14)."""

from __future__ import annotations


def latin_square(grid: list) -> tuple[list | None, int]:
    """Complete an n x n Latin square (each row and column holds 1..n once; 0 = empty) by backtracking.
    Row and column masks make each digit check O(1); the next cell is the one with the fewest options.
    Returns (grid or None, guesses)."""
    n = len(grid)
    full = (1 << n) - 1
    g = [list(r) for r in grid]
    rows, cols = [0] * n, [0] * n
    for r in range(n):
        for c in range(n):
            v = g[r][c]
            if v:
                bit = 1 << (v - 1)
                if rows[r] & bit or cols[c] & bit:
                    return None, 0                    # the givens already break a rule
                rows[r] |= bit
                cols[c] |= bit
    guesses = [0]

    def go():
        best, best_free = None, 0
        for r in range(n):
            for c in range(n):
                if g[r][c] == 0:
                    free = full & ~(rows[r] | cols[c])
                    if best is None or bin(free).count("1") < bin(best_free).count("1"):
                        best, best_free = (r, c), free
        if best is None:
            return True
        r, c = best
        while best_free:
            bit = best_free & -best_free
            best_free -= bit
            guesses[0] += 1
            g[r][c] = bit.bit_length()
            rows[r] |= bit
            cols[c] |= bit
            if go():
                return True
            rows[r] &= ~bit
            cols[c] &= ~bit
            g[r][c] = 0
        return False

    return (g if go() else None), guesses[0]


def queens_shared_set(n: int) -> int:
    """Thinking Problem 3's bug: both diagonal numbers kept in ONE set. Returns the number of solutions found."""
    cols, diags, count = set(), set(), [0]

    def go(r):
        if r == n:
            count[0] += 1
            return
        for c in range(n):
            if c in cols or r - c in diags or r + c in diags:
                continue
            cols.add(c); diags.add(r - c); diags.add(r + c)
            go(r + 1)
            cols.remove(c); diags.discard(r - c); diags.discard(r + c)

    go(0)
    return count[0]
