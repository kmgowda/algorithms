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


def hanoi_with_stack(n: int, source: str, target: str, spare: str,
                     snapshots: list[list[str]] | None = None) -> list[tuple[str, str]]:
    """Hanoi without recursion: a stack of pending tasks replaces the call stack (Figure 14.6).
    A task is ("tower", k, from, to, via) or ("move", from, to). If snapshots is given, the stack's
    contents (bottom to top) are recorded after every pop and push round."""
    moves: list[tuple[str, str]] = []
    tasks: list[tuple] = [("tower", n, source, target, spare)] if n >= 1 else []
    while tasks:
        task = tasks.pop()
        if task[0] == "move":
            moves.append((task[1], task[2]))
        else:
            _, k, a, b, c = task
            if k > 1:
                tasks.append(("tower", k - 1, c, b, a))     # step 3: done last, so pushed first
            tasks.append(("move", a, b))                    # step 2
            if k > 1:
                tasks.append(("tower", k - 1, a, c, b))     # step 1: done first, so pushed last
        if snapshots is not None:
            snapshots.append([describe(t) for t in tasks])
    return moves


def describe(task: tuple) -> str:
    """A short label for a pending task, as drawn in Figure 14.6."""
    if task[0] == "move":
        return f"move {task[1]}\u2192{task[2]}"
    return f"tower {task[1]}: {task[2]}\u2192{task[3]}"


def moves_of_each_disk(n: int) -> list[int]:
    """How many times disks 1 (smallest) to n move in the solution: disk k moves 2^(n-k) times."""
    moves: list[tuple[str, str]] = []
    hanoi(n, "A", "C", "B", moves)
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    counts = [0] * n
    for a, b in moves:
        disk = pegs[a].pop()
        counts[disk - 1] += 1
        pegs[b].append(disk)
    return counts


def adjacent_hanoi(n: int, left: str, right: str, middle: str, moves: list[tuple[str, str]]) -> None:
    """The variant in which a disk may move only to a neighbouring peg (A-B or B-C): carry n disks
    from an end peg to the other end peg through the middle one (Challenge 1)."""
    if n == 0:
        return
    adjacent_hanoi(n - 1, left, right, middle, moves)   # the smaller tower out of the way, to the far end
    moves.append((left, middle))                        # the largest disk one step
    adjacent_hanoi(n - 1, right, left, middle, moves)   # the smaller tower back to the start
    moves.append((middle, right))                       # the largest disk the second step
    adjacent_hanoi(n - 1, left, right, middle, moves)   # the smaller tower on top of it


if __name__ == "__main__":
    moves: list[tuple[str, str]] = []
    hanoi(3, "A", "C", "B", moves)
    print(moves, replay(3, moves))
    four: list[tuple[str, str]] = []
    hanoi(4, "A", "C", "B", four)
    print(len(four), " ".join(f"{a}{b}" for a, b in four))
    print([move_count(n) for n in range(1, 11)], 2 ** 64 - 1)
    print(hanoi_with_stack(3, "A", "C", "B") == moves, moves_of_each_disk(4))
    adj: list[tuple[str, str]] = []
    adjacent_hanoi(3, "A", "C", "B", adj)
    print(len(adj))
