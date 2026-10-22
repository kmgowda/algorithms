"""Volume 6, Chapter 10 - Thinking Problems.

Problem 1: the two-number loop always holds the table's last two entries, so it equals ways_table (checked).
Problem 2: least effort when Leo may climb 1 to k steps at a time, keeping only the last k answers: O(n k) time.
Problem 3: filling the table from the top down reads entries not yet filled and gives wrong counts.
"""

from __future__ import annotations

from collections import deque

from ch10_examples import ways_table


def least_effort_k(effort: list, k: int) -> int:
    if k < 1:
        raise ValueError("Leo must be able to climb at least one step")
    last = deque([0], maxlen=k)                    # least effort to stand on the last k steps (ground first)
    for i in range(1, len(effort) + 2):
        cost = effort[i - 1] if i <= len(effort) else 0
        last.append(min(last) + cost)
    return last[-1]


def wrong_order_table(n: int, steps=(1, 2)) -> list:
    table = [1] + [0] * n
    for i in range(n, 0, -1):                      # the bug: top first
        table[i] = sum(table[i - s] for s in steps if i - s >= 0)
    return table


if __name__ == "__main__":
    from ch10_examples import EFFORT, least_effort
    print(least_effort(EFFORT)[0], least_effort_k(EFFORT, 2), least_effort_k(EFFORT, 3), least_effort_k(EFFORT, 1))
    print(wrong_order_table(6), ways_table(6))
