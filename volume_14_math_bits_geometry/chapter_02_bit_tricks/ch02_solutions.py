"""Volume 14, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations


def reverse_bits(n: int) -> int:
    """Exercise 1 (LeetCode 190): reverse the 32 bits of an unsigned integer."""
    out = 0
    for _ in range(32):
        out = out << 1 | n & 1
        n >>= 1
    return out


def add_without_plus(a: int, b: int) -> int:
    """Exercise 2 (LeetCode 371): XOR adds without carries, AND finds the carries; repeat (32-bit signed)."""
    mask = 0xFFFFFFFF
    while b & mask:
        a, b = a ^ b, (a & b) << 1
    a &= mask
    return a if a < 1 << 31 else a - (1 << 32)


def two_singles(nums: list[int]) -> list[int]:
    """Exercise 3 (LeetCode 260): two numbers appear once, the rest twice. XOR all = x ^ y; split the numbers by
    one bit where x and y differ, and XOR each group."""
    both = 0
    for v in nums:
        both ^= v
    bit = both & -both
    x = 0
    for v in nums:
        if v & bit:
            x ^= v
    return sorted([x, both ^ x])


if __name__ == "__main__":
    print(reverse_bits(0b00000010100101000001111010011100), add_without_plus(-7, 5), two_singles([1, 2, 1, 3, 2, 5]))
