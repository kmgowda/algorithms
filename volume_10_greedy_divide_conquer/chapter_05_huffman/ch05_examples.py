"""Volume 10, Chapter 5 - Huffman Coding: Compressing Files.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import heapq
import itertools
from collections import Counter


def huffman_codes(freq: dict[str, int]) -> dict[str, str]:
    """Greedy: repeatedly merge the two LEAST frequent groups; one side gets a '0', the other a '1'.
    Frequent symbols end up near the root (short codes), rare ones deep (long codes). O(k log k)."""
    if len(freq) == 1:
        return {next(iter(freq)): "0"}
    tie = itertools.count()
    heap = [(f, next(tie), {sym: ""}) for sym, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        merged = {s: "0" + c for s, c in left.items()} | {s: "1" + c for s, c in right.items()}
        heapq.heappush(heap, (f1 + f2, next(tie), merged))
    return heap[0][2]


def encode(text: str, codes: dict[str, str]) -> str:
    return "".join(codes[ch] for ch in text)


def decode(bits: str, codes: dict[str, str]) -> str:
    """Prefix-free codes decode left to right with no separators: no code is the start of another."""
    reverse = {c: s for s, c in codes.items()}
    out, current = [], ""
    for b in bits:
        current += b
        if current in reverse:
            out.append(reverse[current])
            current = ""
    return "".join(out)


def is_prefix_free(codes: dict[str, str]) -> bool:
    words = sorted(codes.values())
    return all(not b.startswith(a) for a, b in zip(words, words[1:]))


def compressed_bits(text: str) -> tuple[int, int]:
    """(bits with Huffman, bits with fixed 8-bit characters)."""
    codes = huffman_codes(Counter(text))
    return len(encode(text, codes)), 8 * len(text)


def fixed_length_bits(text: str) -> int:
    """Practical comparison: the shortest FIXED-length code needs ceil(log2(distinct symbols)) bits each."""
    k = len(set(text))
    width = max(1, (k - 1).bit_length())
    return width * len(text)


if __name__ == "__main__":
    text = "abracadabra"
    codes = huffman_codes(Counter(text))
    bits = encode(text, codes)
    print(codes, "| prefix-free:", is_prefix_free(codes))
    print(bits, "->", decode(bits, codes))
    print("Huffman vs 8-bit:", compressed_bits(text), "| best fixed-length:", fixed_length_bits(text))
    zoo = "the lion and the tiger and the zebra ran to the river " * 20
    h, raw = compressed_bits(zoo)
    print(f"zoo notes: {h} bits instead of {raw} ({100 * h / raw:.0f}%)")
