"""Volume 6, Chapter 9 - Thinking Problems.

Problem 1: plain recursion with steps 1 and 2 makes exactly 2 ways(n + 1) - 1 calls (checked).
Problem 2: climbs that never take two 2-steps in a row, by remembering (stairs left, last step).
Problem 3: a step of size 0 used to make ways_memo recurse for ever; it is now refused.
"""

from __future__ import annotations

from functools import lru_cache


def no_double_two(n: int) -> int:
    @lru_cache(maxsize=None)
    def go(left: int, last: int) -> int:
        if left < 0:
            return 0
        if left == 0:
            return 1
        total = go(left - 1, 1)
        if last != 2:
            total += go(left - 2, 2)
        return total
    return go(n, 0)


def no_double_two_brute(n: int) -> int:
    def climbs(left):
        if left == 0:
            yield ()
        for s in (1, 2):
            if s <= left:
                for rest in climbs(left - s):
                    yield (s,) + rest
    return sum(1 for c in climbs(n) if all(not (a == b == 2) for a, b in zip(c, c[1:])))


if __name__ == "__main__":
    from ch09_examples import plain_calls, ways_memo
    print(plain_calls(10), 2 * ways_memo(11) - 1, [no_double_two(n) for n in range(8)])
