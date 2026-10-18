"""Volume 4, Chapter 12 - Solutions to the exercises."""

from __future__ import annotations

import math

from ch12_examples import ConsistentHashRing, stable_hash


def rendezvous_server(key: str, servers: list[str]) -> str:
    """Exercise 1: rendezvous (highest-random-weight) hashing - each key picks the server with the top score."""
    return max(servers, key=lambda s: stable_hash(f"{s}|{key}"))


def bloom_false_positive_rate(bits: int, hashes: int, items: int) -> float:
    """Exercise 2: the classic estimate (1 - e^(-k*n/m))^k."""
    return (1 - math.exp(-hashes * items / bits)) ** hashes


def best_hash_count(bits: int, items: int) -> int:
    """Exercise 3: the number of hash functions that minimizes false positives, about (m/n) ln 2."""
    return max(1, round(bits / items * math.log(2)))


def keys_moved_on_removal(keys: list[str], servers: list[str], removed: str) -> tuple[int, bool]:
    """Exercise 4: removing a server moves ONLY that server's keys. Returns (moved, only_its_keys_moved)."""
    ring = ConsistentHashRing(servers)
    before = {k: ring.server_for(k) for k in keys}
    ring.remove(removed)
    moved = [k for k in keys if ring.server_for(k) != before[k]]
    return len(moved), all(before[k] == removed for k in moved)


if __name__ == "__main__":
    print(rendezvous_server("user42", ["a", "b", "c"]), round(bloom_false_positive_rate(20_000, 4, 2000), 4))
    print(best_hash_count(20_000, 2000), keys_moved_on_removal([f"k{i}" for i in range(1000)], ["a", "b", "c"], "b"))
