"""Volume 6, Chapter 10 - Bit Tricks and Gray Codes: counting so that only one switch changes at a time.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations


def gray(n: int) -> int:
    """The n-th Gray code: n XOR (n >> 1) (Figure 10.2)."""
    return n ^ (n >> 1)


def from_gray(g: int) -> int:
    """Undo gray(): XOR together every right shift of g."""
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n


def flips(sequence: list) -> list:
    """How many bits change between neighbours."""
    return [bin(a ^ b).count("1") for a, b in zip(sequence, sequence[1:])]


def is_power_of_two(n: int) -> bool:
    return n > 0 and n & (n - 1) == 0


def lowest_bit(n: int) -> int:
    return n & -n


if __name__ == "__main__":
    codes = [gray(i) for i in range(8)]
    print([format(c, "03b") for c in codes], flips(codes), flips(list(range(8))))
    print([from_gray(c) for c in codes], gray(255), from_gray(gray(1000)))
    print([n for n in range(20) if is_power_of_two(n)], lowest_bit(84), lowest_bit(96))
    print(sum(flips(list(range(256)))), sum(flips([gray(i) for i in range(256)])))
