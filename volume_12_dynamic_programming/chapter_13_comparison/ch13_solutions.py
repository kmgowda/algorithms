"""Volume 12, Chapter 13 - Solutions to the exercises."""

from __future__ import annotations

from ch13_examples import choose_paradigm


def classify() -> dict[str, str]:
    """Exercise 1: name the paradigm to try first."""
    return {
        "most meetings in one room": choose_paradigm({"a provably safe local choice"}),
        "sort a billion records on many machines": choose_paradigm({"independent subproblems combined at the end"}),
        "fewest coins with odd coin values": choose_paradigm({"overlapping subproblems with a small state"}),
        "solve a Sudoku": choose_paradigm({"constraints checkable on partial solutions, no small state"}),
        "cheapest tour of 15 cities with a good bound": choose_paradigm({"optimization with a good bound, no small state"}),
    }


def state_size(problem: str) -> str:
    """Exercise 2: the DP state for each problem - if you can't name a small one, DP is the wrong tool."""
    return {
        "weighted jobs": "index of the job in end-time order",
        "edit distance": "(prefix length of a, prefix length of b)",
        "knapsack": "(items considered, capacity left)",
        "TSP": "(set of visited cities as a bitmask, current city)",
        "N-Queens": "no small state - the whole board matters: use backtracking",
    }[problem]


if __name__ == "__main__":
    print(classify())
    print(state_size("TSP"))
