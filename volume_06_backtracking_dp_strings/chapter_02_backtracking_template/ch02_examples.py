"""Volume 6, Chapter 2 - The Backtracking Template: choose, check, explore, undo.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

# Seat readers in a row so that no two who argued sit side by side.
READERS = ["Ana", "Ben", "Cai", "Dev", "Eva", "Fay"]
FEUDS = [("Ana", "Ben"), ("Cai", "Dev"), ("Eva", "Fay"), ("Ana", "Eva")]


def clash(a, b, feuds) -> bool:
    return (a, b) in feuds or (b, a) in feuds


def backtrack(readers: list, feuds: list, row: list, out: list, counter: list) -> None:
    """The template (Section 2.4): try each choice, check it at once, explore, then undo it."""
    counter[0] += 1
    if len(row) == len(readers):
        out.append(list(row))
        return
    for r in readers:
        if r in row:
            continue
        if row and clash(row[-1], r, feuds):
            continue                                  # prune: this branch can never succeed
        row.append(r)                                 # choose
        backtrack(readers, feuds, row, out, counter)  # explore
        row.pop()                                     # undo


def check_at_end(readers: list, feuds: list, row: list, out: list, counter: list) -> None:
    """The same search, checking the rule only when a seating is complete (Chapter 1)."""
    counter[0] += 1
    if len(row) == len(readers):
        if not any(clash(a, b, feuds) for a, b in zip(row, row[1:])):
            out.append(list(row))
        return
    for r in readers:
        if r not in row:
            row.append(r)
            check_at_end(readers, feuds, row, out, counter)
            row.pop()


def first_only(readers: list, feuds: list) -> tuple[list | None, int]:
    """Stop at the first valid seating. Returns (seating, nodes visited)."""
    counter = [0]

    def go(row):
        counter[0] += 1
        if len(row) == len(readers):
            return list(row)
        for r in readers:
            if r not in row and not (row and clash(row[-1], r, feuds)):
                row.append(r)
                found = go(row)
                row.pop()
                if found:
                    return found
        return None

    return go([]), counter[0]


def work(readers: list, feuds: list, early: bool) -> tuple[int, int]:
    """Section 2.5: the total work of a search is (nodes) x (work per node). Count both.
    Returns (nodes, feud checks). early=True checks the new neighbour pair as each seat is filled;
    early=False checks every neighbouring pair of each complete seating."""
    nodes, checks = [0], [0]

    def go(row):
        nodes[0] += 1
        if len(row) == len(readers):
            if not early:
                for a, b in zip(row, row[1:]):
                    checks[0] += 1
                    if clash(a, b, feuds):
                        break
            return
        for r in readers:
            if r in row:
                continue
            if early and row:
                checks[0] += 1
                if clash(row[-1], r, feuds):
                    continue
            go(row + [r])

    go([])
    return nodes[0], checks[0]


def nodes_by_level(readers: list, feuds: list) -> list:
    """How many partial seatings of each length the pruned search visits (Figure 2.2)."""
    counts = [0] * (len(readers) + 1)

    def go(row):
        counts[len(row)] += 1
        if len(row) == len(readers):
            return
        for r in readers:
            if r not in row and not (row and clash(row[-1], r, feuds)):
                go(row + [r])

    go([])
    return counts


if __name__ == "__main__":
    a, ca, b, cb = [], [0], [], [0]
    backtrack(READERS, FEUDS, [], a, ca)
    check_at_end(READERS, FEUDS, [], b, cb)
    print(len(a), ca[0], len(b), cb[0], a == b)
    print(first_only(READERS, FEUDS))
