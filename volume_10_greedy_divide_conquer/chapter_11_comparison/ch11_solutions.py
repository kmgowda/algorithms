"""Volume 10, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

from ch11_examples import choose_paradigm


def classify_problems() -> dict[str, str]:
    """Exercise 1: name the first paradigm to try."""
    return {
        "most talks in one hall": choose_paradigm({"provably safe local choice"}),
        "sort a million records": choose_paradigm({"independent subproblems"}),
        "fewest coins with odd coin values": choose_paradigm({"overlapping subproblems"}),
        "find a word in a dictionary": choose_paradigm({"one smaller instance suffices"}),
        "find duplicate receipts": choose_paradigm({"easier after sorting or restructuring"}),
        "fill a sudoku": choose_paradigm({"must explore combinations with constraints"}),
    }


def count_calls_plain(amount: int, coins: tuple[int, ...]) -> int:
    """Exercise 2: how many calls the plain recursion makes - evidence of overlapping subproblems."""
    if amount == 0:
        return 1
    return 1 + sum(count_calls_plain(amount - c, coins) for c in coins if c <= amount)


if __name__ == "__main__":
    print(classify_problems())
    print([count_calls_plain(n, (1, 3, 4)) for n in (5, 10, 15, 20)])
