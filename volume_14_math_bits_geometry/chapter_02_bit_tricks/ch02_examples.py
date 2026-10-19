"""Volume 14, Chapter 2 - Bit Manipulation Tricks.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

from functools import reduce


def get_bit(n: int, i: int) -> int:
    return n >> i & 1


def set_bit(n: int, i: int) -> int:
    return n | 1 << i


def clear_bit(n: int, i: int) -> int:
    return n & ~(1 << i)


def toggle_bit(n: int, i: int) -> int:
    return n ^ 1 << i


def count_bits(n: int) -> int:
    """LeetCode 191 (Kernighan): n & (n - 1) removes the lowest set bit - loop once per 1-bit."""
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def is_power_of_two(n: int) -> bool:
    """LeetCode 231: a power of two has exactly one set bit."""
    return n > 0 and n & (n - 1) == 0


def lowest_set_bit(n: int) -> int:
    """n & -n isolates the lowest set bit (two's complement trick; used by Fenwick trees, V7-C7)."""
    return n & -n


def single_number(nums: list[int]) -> int:
    """LeetCode 136: every number appears twice except one. x ^ x = 0 and x ^ 0 = x, so XOR everything."""
    return reduce(lambda a, b: a ^ b, nums, 0)


def missing_number(nums: list[int]) -> int:
    """LeetCode 268: 0..n with one missing - XOR all indices and values; pairs cancel."""
    x = len(nums)
    for i, v in enumerate(nums):
        x ^= i ^ v
    return x


def bits_table(n: int) -> list[int]:
    """LeetCode 338: number of 1-bits for every 0..n - bits[i] = bits[i >> 1] + (i & 1)."""
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits


def all_subsets(items: list[str]) -> list[list[str]]:
    """Every subset by counting from 0 to 2^n - 1: bit i says whether item i is in (V12-C10)."""
    n = len(items)
    return [[items[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]


PERMS = {"read": 1, "write": 2, "delete": 4, "admin": 8}


def grant(flags: int, *names: str) -> int:
    """Industry example: permission flags packed into one integer (like Unix file modes)."""
    for name in names:
        flags |= PERMS[name]
    return flags


def can(flags: int, name: str) -> bool:
    return bool(flags & PERMS[name])


if __name__ == "__main__":
    n = 0b1011
    print(get_bit(n, 1), bin(set_bit(n, 2)), bin(clear_bit(n, 0)), bin(toggle_bit(n, 3)))
    print(count_bits(0b1011101), is_power_of_two(64), is_power_of_two(96), bin(lowest_set_bit(0b101000)))
    print(single_number([4, 1, 2, 1, 2]), missing_number([3, 0, 1]), bits_table(8))
    print(all_subsets(["a", "b", "c"]))
    user = grant(0, "read", "write")
    print(bin(user), can(user, "write"), can(user, "delete"))
