"""Volume 6, Chapter 9 - Working with Bits: binary digits, masks, and sets stored in one number.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

FEATURES = ["large print", "audio", "braille", "e-book", "kids", "local history"]


def to_binary(n: int, width: int = 8) -> str:
    if n < 0:
        raise ValueError("this chapter uses whole numbers of 0 or more")
    return format(n, f"0{width}b")


def make_set(names: list) -> int:
    """A set of features as one number: bit i is 1 when FEATURES[i] is present (Figure 9.2)."""
    mask = 0
    for name in names:
        mask |= 1 << FEATURES.index(name)
    return mask


def members(mask: int) -> list:
    return [f for i, f in enumerate(FEATURES) if mask >> i & 1]


def popcount(n: int) -> tuple[int, int]:
    """Count 1 bits by clearing the lowest one each time (n & (n - 1)). Returns (count, steps)."""
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count, count


def subsets(mask: int) -> list:
    """Every subset of a mask, by the trick sub = (sub - 1) & mask."""
    out, sub = [], mask
    while True:
        out.append(sub)
        if sub == 0:
            return out
        sub = (sub - 1) & mask


if __name__ == "__main__":
    print(to_binary(5), to_binary(84), to_binary(255))
    a, b = make_set(["large print", "audio", "kids"]), make_set(["audio", "e-book", "kids"])
    print(a, b, to_binary(a), to_binary(b), members(a & b), members(a | b), members(a ^ b), members(a & ~b))
    print(popcount(84), popcount(2 ** 40 - 1), popcount(0), len(subsets(a)), [members(s) for s in subsets(make_set(["audio", "kids"]))])
