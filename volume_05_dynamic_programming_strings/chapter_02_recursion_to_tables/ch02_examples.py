"""Volume 5, Chapter 2 - From Recursion to Tables: fill the answers from the bottom up.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

# Effort to stand on each step of the library stairs (step 1 first); the top is free.
EFFORT = [3, 9, 2, 7, 4, 8, 1, 6]


def ways_table(n: int, steps=(1, 2)) -> list:
    """Ways to reach every step 0..n, filled bottom-up (Figure 2.1)."""
    table = [1] + [0] * n
    for i in range(1, n + 1):
        table[i] = sum(table[i - s] for s in steps if i - s >= 0)
    return table


def ways_two_numbers(n: int) -> int:
    """Steps of 1 or 2 keep only the last two answers: constant memory."""
    a, b = 1, 1                                       # ways to reach i - 2 and i - 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b if n >= 1 else 1


def least_effort(effort: list) -> tuple[int, list, list]:
    """Least total effort to reach the top (one past the last step), moving up 1 or 2 steps (Figure 2.3).
    Returns (total, table, steps stood on)."""
    n = len(effort)
    best = [0] * (n + 2)                              # best[i]: least effort to stand on step i (0 = ground)
    came = [0] * (n + 2)
    for i in range(1, n + 2):
        cost = effort[i - 1] if i <= n else 0
        options = [(best[i - 1], i - 1)] + ([(best[i - 2], i - 2)] if i >= 2 else [])
        b, frm = min(options)
        best[i], came[i] = b + cost, frm
    path, i = [], came[n + 1]
    while i > 0:
        path.append(i)
        i = came[i]
    return best[n + 1], best, path[::-1]


if __name__ == "__main__":
    print(ways_table(10))
    print(ways_two_numbers(10), ways_two_numbers(1), ways_two_numbers(0))
    print(len(str(ways_table(5000)[-1])))
    print(least_effort(EFFORT))
