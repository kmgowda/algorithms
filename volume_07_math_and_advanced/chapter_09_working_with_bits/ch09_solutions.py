"""Volume 7, Chapter 9 - Thinking Problems.

Problem 1: n & (n - 1) == 0 exactly when n is 0 or a power of two (checked for every n below 2^16).
Problem 2: the number of 1 bits of every number 0 .. N in O(N), from ones[i] = ones[i >> 1] + (i & 1).
Problem 3: the subset loop 'while sub: ...' forgets the empty subset, and the fix.
"""

from __future__ import annotations


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def ones_up_to(limit: int) -> list:
    """ones[i] = number of 1 bits of i, for i = 0 .. limit, each from the entry for i >> 1."""
    if limit < 0:
        return []
    ones = [0] * (limit + 1)
    for i in range(1, limit + 1):
        ones[i] = ones[i >> 1] + (i & 1)
    return ones


def buggy_subsets(mask: int) -> list:
    """Looks tidy, but stops before recording the empty subset."""
    out, sub = [], mask
    while sub:
        out.append(sub)
        sub = (sub - 1) & mask
    return out


def subsets_fixed(mask: int) -> list:
    out = buggy_subsets(mask)
    out.append(0)                               # the empty subset is a subset too
    return out


if __name__ == "__main__":
    print(ones_up_to(16), sum(ones_up_to(255)))
    print(buggy_subsets(0b10010), subsets_fixed(0b10010), buggy_subsets(0))
