"""Volume 11, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations


def dice_rolls_with_total(dice: int, target: int) -> list[tuple[int, ...]]:
    """Exercise 1: every sequence of dice rolls (1-6) with the given total - stop early when the total is exceeded."""
    out: list[tuple[int, ...]] = []

    def go(rolls: tuple[int, ...], total: int) -> None:
        if total > target:
            return
        if len(rolls) == dice:
            if total == target:
                out.append(rolls)
            return
        for face in range(1, 7):
            go(rolls + (face,), total + face)

    go((), 0)
    return out


def leaves_and_nodes(depth: int, branching: int) -> tuple[int, int]:
    """Exercise 2: leaves and total nodes of a full tree."""
    leaves = branching ** depth
    nodes = sum(branching ** k for k in range(depth + 1))
    return leaves, nodes


def pin_codes(length: int, digits: str = "0123456789") -> int:
    """Exercise 3: how many PIN codes - the number of leaves when each level offers len(digits) choices."""
    return len(digits) ** length


if __name__ == "__main__":
    print(len(dice_rolls_with_total(3, 10)), leaves_and_nodes(3, 2), pin_codes(4))
