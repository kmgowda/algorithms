"""Volume 1, Chapter 14, Thinking Problem 2 - which disk makes move number m, without listing the moves.

The moves of Hanoi(n) are the moves of Hanoi(n - 1) to the spare, then the largest disk, then the moves of
Hanoi(n - 1) back on top. So move m is found by deciding, at each size, whether m falls in the first half,
is the middle move, or falls in the second half: at most n calls, however many moves there are.

Run:  python3 ch14_solutions.py
"""

from __future__ import annotations


def move_number(n: int, m: int, source: str, target: str, spare: str) -> tuple[int, str, str]:
    """(disk, from, to) of move m (1 <= m <= 2^n - 1) of the n-disk solution from source to target."""
    if not 1 <= m <= 2 ** n - 1:
        raise ValueError("move number out of range")
    half = 2 ** (n - 1)
    if m == half:
        return n, source, target                                 # the middle move: the largest disk
    if m < half:
        return move_number(n - 1, m, source, spare, target)       # inside step 1
    return move_number(n - 1, m - half, spare, target, source)    # inside step 3


if __name__ == "__main__":
    print([move_number(4, m, "A", "C", "B") for m in range(1, 16)])
    print(move_number(64, 10 ** 12, "A", "C", "B"))
