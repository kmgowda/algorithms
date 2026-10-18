"""Volume 4, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch02_examples import ChainedHashMap


class HashSet:
    """Exercise 1 (LeetCode 705): a set built on ChainedHashMap - keys only, value ignored."""

    def __init__(self) -> None:
        self._map = ChainedHashMap()

    def add(self, key: Hashable) -> None:
        self._map[key] = True

    def remove(self, key: Hashable) -> None:
        if key in self._map:
            del self._map[key]

    def __contains__(self, key: Hashable) -> bool:
        return key in self._map

    def __len__(self) -> int:
        return len(self._map)


def expected_probes_linear(load: float) -> tuple[float, float]:
    """Exercise 3: Knuth's classic estimates for linear probing (successful, unsuccessful search)."""
    if not 0 <= load < 1:
        raise ValueError("load factor must be in [0, 1)")
    hit = 0.5 * (1 + 1 / (1 - load))
    miss = 0.5 * (1 + 1 / (1 - load) ** 2)
    return round(hit, 2), round(miss, 2)


class BadKey:
    """Exercise 4: every BadKey hashes to the same slot - the worst case."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __hash__(self) -> int:
        return 42

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BadKey) and other.name == self.name


def worst_case_chain(n: int) -> int:
    """Insert n BadKeys and report the longest chain (it equals n: lookups become O(n))."""
    table = ChainedHashMap()
    for i in range(n):
        table[BadKey(str(i))] = i
    return table.longest_chain()


if __name__ == "__main__":
    s = HashSet()
    for x in (1, 2, 2, 3):
        s.add(x)
    s.remove(2)
    print(len(s), 2 in s, expected_probes_linear(0.5), expected_probes_linear(0.9), worst_case_chain(50))
