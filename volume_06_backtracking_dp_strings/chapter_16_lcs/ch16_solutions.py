"""Volume 6, Chapter 16 - Thinking Problems.

Problem 1: when the last items match, some longest common subsequence ends with that match (checked).
Problem 2: the shortest list containing both reading lists in order has n + m - LCS items; build it from the table.
Problem 3: matching greedily (each item of a with its first possible place in b) can miss the longest; a counterexample.
"""

from __future__ import annotations

import itertools

from ch16_examples import lcs


def shortest_super(a, b) -> list:
    _, _, L = lcs(a, b)
    out, i, j = [], len(a), len(b)
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1]); i -= 1; j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            out.append(a[i - 1]); i -= 1
        else:
            out.append(b[j - 1]); j -= 1
    out += list(reversed(a[:i])) + list(reversed(b[:j]))
    return out[::-1]


def is_subsequence(small, big) -> bool:
    it = iter(big)
    return all(x in it for x in small)


def greedy_common(a, b) -> int:
    count, pos = 0, 0
    for x in a:
        try:
            k = list(b).index(x, pos)
        except ValueError:
            continue
        count, pos = count + 1, k + 1
    return count


def greedy_trap() -> tuple:
    for n in range(1, 5):
        for a in itertools.product("AB", repeat=n):
            for b in itertools.product("AB", repeat=n):
                if greedy_common(a, b) < lcs(a, b)[0]:
                    return "".join(a), "".join(b)
    return None


if __name__ == "__main__":
    from ch16_examples import ANA, BEN
    s = shortest_super(ANA, BEN)
    print(len(s), s, greedy_trap(), greedy_common(ANA, BEN), lcs(ANA, BEN)[0])
