"""Volume 4, Chapter 2 - Hash Tables: Collisions, Chaining, Open Addressing, Resizing.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

from typing import Any, Hashable, Iterator


class ChainedHashMap:
    """Separate chaining: each slot holds a small list ("chain") of (key, value) pairs.

    Invariants: every key appears at most once; a key lives in chain hash(key) % len(slots);
    load factor (size / slots) stays <= MAX_LOAD by doubling the slot count.
    """

    MAX_LOAD = 1.0

    def __init__(self, slots: int = 8) -> None:
        self._slots: list[list[tuple[Hashable, Any]]] = [[] for _ in range(slots)]
        self._size = 0
        self.resizes = 0

    def _chain(self, key: Hashable) -> list[tuple[Hashable, Any]]:
        return self._slots[hash(key) % len(self._slots)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        chain = self._chain(key)
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)            # update an existing key
                return
        chain.append((key, value))
        self._size += 1
        if self._size / len(self._slots) > self.MAX_LOAD:
            self._resize(2 * len(self._slots))

    def __getitem__(self, key: Hashable) -> Any:
        for k, v in self._chain(key):
            if k == key:
                return v
        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        chain = self._chain(key)
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self._size -= 1
                return
        raise KeyError(key)

    def __contains__(self, key: Hashable) -> bool:
        return any(k == key for k, _ in self._chain(key))

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Hashable]:
        for chain in self._slots:
            for k, _ in chain:
                yield k

    def _resize(self, new_slots: int) -> None:
        old = [pair for chain in self._slots for pair in chain]
        self._slots = [[] for _ in range(new_slots)]
        for k, v in old:                           # every key must move: its slot depends on the table size
            self._slots[hash(k) % new_slots].append((k, v))
        self.resizes += 1

    def longest_chain(self) -> int:
        return max(len(chain) for chain in self._slots)

    @property
    def load_factor(self) -> float:
        return self._size / len(self._slots)


_EMPTY = object()      # never used
_DELETED = object()    # a "tombstone": something was here; keep probing past it


class OpenAddressingHashMap:
    """Open addressing with linear probing: on a collision, try the next slot, and the next...

    Invariants: load factor <= MAX_LOAD (counting tombstones), so an empty slot always exists
    and every search terminates.
    """

    MAX_LOAD = 0.6

    def __init__(self, slots: int = 8) -> None:
        self._keys: list[Any] = [_EMPTY] * slots
        self._values: list[Any] = [None] * slots
        self._size = 0
        self._used = 0                             # live keys + tombstones
        self.probes = 0                            # for teaching: how many slots were inspected

    def _find(self, key: Hashable) -> tuple[int, bool]:
        """Return (slot, found). If not found, slot is where the key should be inserted."""
        n = len(self._keys)
        i = hash(key) % n
        first_tombstone = -1
        while True:
            self.probes += 1
            k = self._keys[i]
            if k is _EMPTY:
                return (first_tombstone if first_tombstone >= 0 else i), False
            if k is _DELETED:
                if first_tombstone < 0:
                    first_tombstone = i
            elif k == key:
                return i, True
            i = (i + 1) % n                        # linear probing: try the next slot

    def __setitem__(self, key: Hashable, value: Any) -> None:
        slot, found = self._find(key)
        if found:
            self._values[slot] = value
            return
        if self._keys[slot] is _EMPTY:
            self._used += 1
        self._keys[slot] = key
        self._values[slot] = value
        self._size += 1
        if self._used / len(self._keys) > self.MAX_LOAD:
            self._resize(2 * len(self._keys))

    def __getitem__(self, key: Hashable) -> Any:
        slot, found = self._find(key)
        if not found:
            raise KeyError(key)
        return self._values[slot]

    def __delitem__(self, key: Hashable) -> None:
        slot, found = self._find(key)
        if not found:
            raise KeyError(key)
        self._keys[slot] = _DELETED                # can't just empty it: that would break probe chains
        self._values[slot] = None
        self._size -= 1

    def __contains__(self, key: Hashable) -> bool:
        return self._find(key)[1]

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Hashable]:
        for k in self._keys:
            if k is not _EMPTY and k is not _DELETED:
                yield k

    def _resize(self, new_slots: int) -> None:
        pairs = [(k, v) for k, v in zip(self._keys, self._values) if k is not _EMPTY and k is not _DELETED]
        self._keys = [_EMPTY] * new_slots
        self._values = [None] * new_slots
        self._size = self._used = 0
        for k, v in pairs:                         # rehashing also clears out tombstones
            self[k] = v


def stock_levels(deliveries: list[tuple[str, int]]) -> ChainedHashMap:
    """Practical example: a shop's stock counts by product code."""
    stock = ChainedHashMap()
    for code, qty in deliveries:
        stock[code] = stock.get(code, 0) + qty
    return stock


if __name__ == "__main__":
    zoo = ChainedHashMap(slots=4)
    for i, animal in enumerate(["lion", "zebra", "otter", "panda", "koala", "tiger", "camel"]):
        zoo[animal] = i
    print(f"chained: size={len(zoo)} slots={len(zoo._slots)} resizes={zoo.resizes} "
          f"load={zoo.load_factor:.2f} longest chain={zoo.longest_chain()}")
    del zoo["otter"]
    print("otter" in zoo, zoo["panda"], sorted(zoo))
    oa = OpenAddressingHashMap()
    for i in range(1000):
        oa[f"seat-{i}"] = i
    oa.probes = 0
    for i in range(1000):
        _ = oa[f"seat-{i}"]
    print(f"open addressing: 1000 lookups took {oa.probes} probes (about {oa.probes / 1000:.2f} each)")
    print("Stock:", {code: stock_levels([("MILK", 20), ("EGGS", 12), ("MILK", 5)])[code] for code in ("MILK", "EGGS")})
