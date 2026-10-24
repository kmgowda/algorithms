"""Volume 7, Chapter 9 - Working with Bits: binary digits, masks, and sets stored in one number.

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


BYTE_COUNTS = [bin(i).count("1") for i in range(256)]


def popcount_by_table(n: int) -> tuple[int, int]:
    """Count 1 bits a byte at a time with a 256-entry table. Returns (count, table lookups)."""
    count, lookups = 0, 0
    while n:
        count += BYTE_COUNTS[n & 0xFF]
        n >>= 8
        lookups += 1
    return count, lookups


class Bitset:
    """A set of the numbers 0..size-1 packed 64 to a word."""

    def __init__(self, size: int) -> None:
        if size < 0:
            raise ValueError("size must be 0 or more")
        self.size = size
        self.words = [0] * ((size + 63) // 64)

    def add(self, i: int) -> None:
        self.words[i >> 6] |= 1 << (i & 63)

    def __contains__(self, i: int) -> bool:
        return 0 <= i < self.size and self.words[i >> 6] >> (i & 63) & 1 == 1

    def union(self, other: "Bitset") -> "Bitset":
        out = Bitset(self.size)
        out.words = [a | b for a, b in zip(self.words, other.words)]
        return out

    def intersection(self, other: "Bitset") -> "Bitset":
        out = Bitset(self.size)
        out.words = [a & b for a, b in zip(self.words, other.words)]
        return out

    def count(self) -> int:
        return sum(bin(w).count("1") for w in self.words)


def next_same_popcount(n: int) -> int:
    """Gosper's hack: the next larger number with the same number of 1 bits (n > 0)."""
    c = n & -n
    r = n + c
    return r | (((n ^ r) // c) >> 2)


BRANCHES = {"North": 0b010011, "East": 0b011010, "South": 0b100101, "West": 0b001100, "Harbour": 0b110000}


def fewest_branches_covering(target: int, branches: dict = BRANCHES) -> tuple[list, int]:
    """Try all 2^b groups of branches (as masks over the branch list) and return the smallest group whose features
    together include every feature in target. Returns (names, groups tried)."""
    names = list(branches)
    best, tried = None, 0
    for group in range(1 << len(names)):
        tried += 1
        covered = 0
        for i, name in enumerate(names):
            if group >> i & 1:
                covered |= branches[name]
        if covered & target == target and (best is None or bin(group).count("1") < bin(best).count("1")):
            best = group
    if best is None:
        return [], tried
    return [n for i, n in enumerate(names) if best >> i & 1], tried


def nim_winner(piles: list) -> tuple[bool, list]:
    """Nim: take any number of books from one pile; whoever takes the last book wins. The player to move wins
    exactly when the XOR of the pile sizes is not 0 (Bouton, 1901). Returns (mover wins?, a winning move
    (pile index, new size) or [])."""
    x = 0
    for p in piles:
        x ^= p
    if x == 0:
        return False, []
    for i, p in enumerate(piles):
        if p ^ x < p:
            return True, [i, p ^ x]
    return True, []


def grundy(n: int, moves: list, memo: dict | None = None) -> int:
    """Grundy number of a pile of n when a move removes any amount in `moves`: the smallest whole number not
    among the Grundy numbers of the positions one move away (Sprague and Grundy, 1930s)."""
    memo = {} if memo is None else memo
    if n not in memo:
        reach = {grundy(n - m, moves, memo) for m in moves if m <= n}
        g = 0
        while g in reach:
            g += 1
        memo[n] = g
    return memo[n]


def sum_winner(piles: list, moves: list) -> bool:
    """A sum of games (several piles, each with the same move rule): the mover wins exactly when the XOR of
    the piles' Grundy numbers is not 0."""
    x = 0
    for p in piles:
        x ^= grundy(p, moves)
    return x != 0


if __name__ == "__main__":
    print(to_binary(5), to_binary(84), to_binary(255))
    a, b = make_set(["large print", "audio", "kids"]), make_set(["audio", "e-book", "kids"])
    print(a, b, to_binary(a), to_binary(b), members(a & b), members(a | b), members(a ^ b), members(a & ~b))
    print(popcount(84), popcount(2 ** 40 - 1), popcount(0), len(subsets(a)), [members(s) for s in subsets(make_set(["audio", "kids"]))])
    print(subsets(a), [to_binary(x, 6) for x in subsets(a)], popcount_by_table(2 ** 40 - 1), popcount_by_table(84))
    bs = Bitset(1000)
    for x in range(0, 1000, 7):
        bs.add(x)
    other = Bitset(1000)
    for x in range(0, 1000, 11):
        other.add(x)
    print(bs.count(), other.count(), bs.intersection(other).count(), bs.union(other).count(), len(bs.words), 77 in bs.intersection(other))
    print(fewest_branches_covering(0b111111), fewest_branches_covering(make_set(["braille", "local history"])))
    print(84 - 1, to_binary(84), to_binary(83), to_binary(84 & 83))
    print(nim_winner([3, 4, 5]), [grundy(n, [1, 2, 3]) for n in range(9)], sum_winner([5, 7], [1, 3, 4]))
