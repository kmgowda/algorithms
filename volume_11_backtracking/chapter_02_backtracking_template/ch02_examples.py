"""Volume 11, Chapter 2 - The Backtracking Template: Choose, Explore, Un-choose.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def backtrack(state: list[T],
              is_complete: Callable[[list[T]], bool],
              options: Callable[[list[T]], Iterable[T]],
              is_valid: Callable[[list[T]], bool],
              results: list[list[T]]) -> None:
    """The universal template.
    1. If the partial solution is complete, record a COPY.
    2. Otherwise, for each option: CHOOSE it, check it, EXPLORE deeper, then UN-CHOOSE it."""
    if is_complete(state):
        results.append(list(state))
        return
    for option in options(state):
        state.append(option)                 # choose
        if is_valid(state):
            backtrack(state, is_complete, options, is_valid, results)   # explore
        state.pop()                          # un-choose


def arrangements(people: list[str]) -> list[list[str]]:
    """Beginner example: every seating order - options are the people not yet seated."""
    out: list[list[str]] = []
    backtrack([], lambda s: len(s) == len(people), lambda s: [p for p in people if p not in s], lambda s: True, out)
    return out


def no_adjacent_rivals(people: list[str], rivals: set[frozenset[str]]) -> list[list[str]]:
    """Practical example: seating orders where no two rivals sit side by side - checked as soon as someone sits."""
    out: list[list[str]] = []
    backtrack([], lambda s: len(s) == len(people),
              lambda s: [p for p in people if p not in s],
              lambda s: len(s) < 2 or frozenset(s[-2:]) not in rivals, out)
    return out


def binary_strings_without_11(n: int) -> list[str]:
    """Strings of n bits with no two 1s in a row (e.g. no two adjacent rooms booked)."""
    out: list[list[str]] = []
    backtrack([], lambda s: len(s) == n, lambda s: "01",
              lambda s: not (len(s) >= 2 and s[-1] == s[-2] == "1"), out)
    return ["".join(s) for s in out]


def maze_paths(grid: list[str]) -> list[list[tuple[int, int]]]:
    """All simple paths from top-left to bottom-right through '.' cells (4 directions).
    The 'visited' marks are chosen and un-chosen along with the path."""
    rows, cols = len(grid), len(grid[0])
    paths: list[list[tuple[int, int]]] = []
    path: list[tuple[int, int]] = [(0, 0)]
    visited = {(0, 0)}

    def explore(r: int, c: int) -> None:
        if (r, c) == (rows - 1, cols - 1):
            paths.append(list(path))
            return
        for nr, nc in ((r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "." and (nr, nc) not in visited:
                visited.add((nr, nc))
                path.append((nr, nc))          # choose
                explore(nr, nc)                # explore
                path.pop()                     # un-choose
                visited.remove((nr, nc))

    if grid[0][0] == ".":
        explore(0, 0)
    return paths


def test_case_combinations(settings: dict[str, list[str]], forbidden: list[dict[str, str]]) -> list[dict[str, str]]:
    """Industry example: QA engineers list every combination of settings, skipping known-impossible pairs."""
    names = list(settings)
    out: list[list[str]] = []

    def ok(s: list[str]) -> bool:
        current = dict(zip(names, s))
        return not any(all(current.get(k) == v for k, v in rule.items()) for rule in forbidden)

    backtrack([], lambda s: len(s) == len(names), lambda s: settings[names[len(s)]], ok, out)
    return [dict(zip(names, s)) for s in out]


if __name__ == "__main__":
    print(len(arrangements(["Asha", "Ben", "Cy"])), arrangements(["Asha", "Ben", "Cy"])[:2])
    print(no_adjacent_rivals(["Asha", "Ben", "Cy"], {frozenset({"Asha", "Ben"})}))
    print(binary_strings_without_11(4))
    print(len(maze_paths(["...", ".#.", "..."])), "maze paths")
    tests = test_case_combinations({"os": ["linux", "mac"], "browser": ["chrome", "safari"], "lang": ["en", "hi"]},
                                   [{"os": "linux", "browser": "safari"}])
    print(len(tests), "test combinations")
