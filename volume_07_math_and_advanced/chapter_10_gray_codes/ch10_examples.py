"""Volume 7, Chapter 10 - Bit Tricks and Gray Codes: counting so that only one switch changes at a time.

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


def reflected(bits: int) -> list:
    """The reflected Gray code built by reflection (Figure 10.2): list the (bits-1)-bit code, then its mirror image,
    prefixing 0s to the first half and 1s to the second."""
    codes = [0]
    for b in range(bits):
        codes = codes + [c | (1 << b) for c in reversed(codes)]
    return codes


def binary_flips_counting_to(n: int) -> int:
    """Total bits flipped when a binary counter goes 0, 1, ..., n: 2n - popcount(n)."""
    return 2 * n - bin(n).count("1")


def changed_bit(k: int) -> int:
    """Going from gray(k - 1) to gray(k) flips exactly one bit: the position of the lowest 1 bit of k."""
    return (k & -k).bit_length() - 1


def gray_walk(bits: int) -> list:
    """Generate all Gray codes in order, flipping one bit per step (the lowest set bit of the step number)."""
    g, out = 0, [0]
    for k in range(1, 1 << bits):
        g ^= k & -k
        out.append(g)
    return out


def hanoi_by_gray(disks: int) -> list:
    """Tower of Hanoi moves: at step k move the disk numbered changed_bit(k) + 1 (disk 1 is the smallest)."""
    return [changed_bit(k) + 1 for k in range(1, 1 << disks)]


if __name__ == "__main__":
    codes = [gray(i) for i in range(8)]
    print([format(c, "03b") for c in codes], flips(codes), flips(list(range(8))))
    print([from_gray(c) for c in codes], gray(255), from_gray(gray(1000)))
    print([n for n in range(20) if is_power_of_two(n)], lowest_bit(84), lowest_bit(96))
    print(sum(flips(list(range(256)))), sum(flips([gray(i) for i in range(256)])))
    print(reflected(3), reflected(3) == codes, binary_flips_counting_to(255), binary_flips_counting_to(1023), sum(flips(list(range(1024)))))
    print([changed_bit(k) for k in range(1, 8)], gray_walk(3) == codes, hanoi_by_gray(3))
