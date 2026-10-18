"""Volume 10, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

import heapq
from functools import lru_cache

from ch05_examples import huffman_codes


def weighted_length(freq: dict[str, int], codes: dict[str, str]) -> int:
    """Exercise 1: total encoded bits = sum of frequency x code length."""
    return sum(freq[s] * len(codes[s]) for s in freq)


def huffman_cost_only(freq: list[int]) -> int:
    """Exercise 2: the total bits without building codes - the sum of all merge totals (like rope joining, LeetCode 1167)."""
    heap = list(freq)
    heapq.heapify(heap)
    cost = 0
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        cost += a + b
        heapq.heappush(heap, a + b)
    return cost


def best_prefix_code_brute(freq: dict[str, int]) -> int:
    """Exercise 3: optimal total bits by trying every full binary tree shape (tiny alphabets).
    Recursively split the symbol set into two non-empty groups; each level adds one bit to everyone below."""
    symbols = tuple(sorted(freq))

    @lru_cache(maxsize=None)
    def best(group: tuple[str, ...]) -> int:
        if len(group) == 1:
            return 0
        total = sum(freq[s] for s in group)
        options = []
        n = len(group)
        for mask in range(1, (1 << n) - 1):
            if mask & 1:                                  # avoid counting each split twice
                left = tuple(group[i] for i in range(n) if mask >> i & 1)
                right = tuple(group[i] for i in range(n) if not mask >> i & 1)
                options.append(best(left) + best(right))
        return total + min(options)
    return best(symbols)


def canonical_codes(freq: dict[str, int]) -> dict[str, str]:
    """Exercise 4 (industry): store only code LENGTHS (as ZIP/JPEG do) and rebuild codes in a fixed order."""
    lengths = {s: len(c) for s, c in huffman_codes(freq).items()}
    code, prev_len, out = 0, 0, {}
    for s in sorted(lengths, key=lambda s: (lengths[s], s)):
        code <<= lengths[s] - prev_len
        out[s] = format(code, f"0{lengths[s]}b")
        code += 1
        prev_len = lengths[s]
    return out


if __name__ == "__main__":
    f = {"a": 5, "b": 2, "r": 2, "c": 1, "d": 1}
    print(weighted_length(f, huffman_codes(f)), huffman_cost_only(list(f.values())), best_prefix_code_brute(f))
    print(canonical_codes(f))
