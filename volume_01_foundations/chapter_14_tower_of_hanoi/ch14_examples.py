"""Volume 1, Chapter 14 - The Tower of Hanoi.

Run:  python3 ch14_examples.py
"""

from __future__ import annotations


def hanoi(n: int, source: str, target: str, spare: str, moves: list[tuple[str, str]]) -> None:
    """Append the moves that carry n disks from source to target (Figure 14.3)."""
    if n == 0:
        return
    hanoi(n - 1, source, spare, target, moves)
    moves.append((source, target))
    hanoi(n - 1, spare, target, source, moves)


def replay(n: int, moves: list[tuple[str, str]]) -> dict[str, list[int]]:
    """Carry out the moves on real pegs, checking every rule; returns the final pegs."""
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    for a, b in moves:
        assert pegs[a], f"no disk on {a}"
        disk = pegs[a][-1]
        assert not pegs[b] or pegs[b][-1] > disk, f"disk {disk} would land on a smaller disk"
        pegs[b].append(pegs[a].pop())
    return pegs


def move_count(n: int) -> int:
    """M(n) = 2 M(n - 1) + 1 with M(0) = 0, which equals 2^n - 1."""
    return 0 if n == 0 else 2 * move_count(n - 1) + 1


if __name__ == "__main__":
    moves: list[tuple[str, str]] = []
    hanoi(3, "A", "C", "B", moves)
    print(moves, replay(3, moves))
    four: list[tuple[str, str]] = []
    hanoi(4, "A", "C", "B", four)
    print(len(four), " ".join(f"{a}{b}" for a, b in four))
    print([move_count(n) for n in range(1, 11)], 2 ** 64 - 1)
