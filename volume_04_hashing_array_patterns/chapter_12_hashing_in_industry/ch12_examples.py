"""Volume 4, Chapter 12 - Hashing in Industry: Sharding, Consistent Hashing, Bloom Filters.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import bisect
import hashlib
from collections import Counter


def stable_hash(text: str) -> int:
    """A hash that is the SAME on every machine and every run (unlike Python's randomized hash())."""
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")


def mod_shard(key: str, servers: int) -> int:
    """Simple sharding: server = hash mod N. Easy - but changing N moves almost every key."""
    return stable_hash(key) % servers


def moved_fraction_mod(keys: list[str], old_n: int, new_n: int) -> float:
    return sum(mod_shard(k, old_n) != mod_shard(k, new_n) for k in keys) / len(keys)


class ConsistentHashRing:
    """Servers and keys are hashed onto the same circle; a key belongs to the next server clockwise.

    Adding or removing a server only moves the keys in its arc. 'Virtual nodes' (several points per
    server) spread the load evenly.
    """

    def __init__(self, servers: list[str], replicas: int = 100) -> None:
        self.replicas = replicas
        self._points: list[int] = []
        self._owner: dict[int, str] = {}
        for server in servers:
            self.add(server)

    def add(self, server: str) -> None:
        for i in range(self.replicas):
            point = stable_hash(f"{server}#{i}")
            bisect.insort(self._points, point)
            self._owner[point] = server

    def remove(self, server: str) -> None:
        for i in range(self.replicas):
            point = stable_hash(f"{server}#{i}")
            self._points.remove(point)
            del self._owner[point]

    def server_for(self, key: str) -> str:
        if not self._points:
            raise LookupError("no servers")
        i = bisect.bisect_right(self._points, stable_hash(key)) % len(self._points)   # wrap around the circle
        return self._owner[self._points[i]]


def moved_fraction_ring(keys: list[str], servers: list[str], new_server: str, replicas: int = 100) -> float:
    ring = ConsistentHashRing(servers, replicas)
    before = {k: ring.server_for(k) for k in keys}
    ring.add(new_server)
    return sum(ring.server_for(k) != before[k] for k in keys) / len(keys)


def load_spread(keys: list[str], ring: ConsistentHashRing) -> dict[str, int]:
    return dict(Counter(ring.server_for(k) for k in keys))


class BloomFilter:
    """'Definitely not present' or 'probably present', using a bit array and k hash functions.

    No false negatives; a small, tunable rate of false positives; far less memory than a set.
    """

    def __init__(self, bits: int, hashes: int) -> None:
        self.bits = bits
        self.hashes = hashes
        self._array = bytearray((bits + 7) // 8)

    def _positions(self, item: str) -> list[int]:
        return [stable_hash(f"{i}:{item}") % self.bits for i in range(self.hashes)]

    def add(self, item: str) -> None:
        for p in self._positions(item):
            self._array[p // 8] |= 1 << (p % 8)

    def might_contain(self, item: str) -> bool:
        return all(self._array[p // 8] & (1 << (p % 8)) for p in self._positions(item))


if __name__ == "__main__":
    users = [f"user{i}" for i in range(20_000)]
    print(f"mod-N sharding, 4 -> 5 servers: {moved_fraction_mod(users, 4, 5):.0%} of keys move")
    servers = ["db-a", "db-b", "db-c", "db-d"]
    print(f"consistent hashing, add a 5th: {moved_fraction_ring(users, servers, 'db-e'):.0%} of keys move")
    print("Load per server:", load_spread(users, ConsistentHashRing(servers)))
    bloom = BloomFilter(bits=20_000, hashes=4)
    for name in users[:2000]:
        bloom.add(name)
    false_pos = sum(bloom.might_contain(f"stranger{i}") for i in range(5000)) / 5000
    print("Every added user found:", all(bloom.might_contain(u) for u in users[:2000]),
          f"| false-positive rate: {false_pos:.1%}")
