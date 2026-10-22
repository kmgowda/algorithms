"""Volume 5, Chapter 16 - Huffman Coding: short codes for common letters, built greedily.

Run:  python3 ch16_examples.py
"""

from __future__ import annotations

import heapq
import itertools
from collections import Counter

MESSAGE = "LIBRARY BOOK SALE"


def huffman_codes(text: str, log: list | None = None) -> dict:
    """Repeatedly join the two rarest groups (Figure 16.2); the joins form a tree whose paths are the codes."""
    counts = Counter(text)
    if not counts:
        return {}                                     # nothing to encode
    if len(counts) == 1:
        return {next(iter(counts)): "0"}
    tick = itertools.count()                          # breaks ties so the heap never compares dictionaries
    heap = [(n, next(tick), {ch: ""}) for ch, n in sorted(counts.items())]
    heapq.heapify(heap)
    while len(heap) > 1:
        n1, _, a = heapq.heappop(heap)
        n2, _, b = heapq.heappop(heap)
        if log is not None:
            log.append((n1, "".join(sorted(a)), n2, "".join(sorted(b))))
        merged = {ch: "0" + c for ch, c in a.items()}
        merged.update({ch: "1" + c for ch, c in b.items()})
        heapq.heappush(heap, (n1 + n2, next(tick), merged))
    return heap[0][2]


def encode(text: str, codes: dict) -> str:
    return "".join(codes[ch] for ch in text)


def decode(bits: str, codes: dict) -> str:
    back, out, cur = {c: ch for ch, c in codes.items()}, [], ""
    for b in bits:
        cur += b
        if cur in back:
            out.append(back[cur])
            cur = ""
    return "".join(out)


def fixed_bits(text: str) -> int:
    """Bits with a fixed-length code: enough bits per letter to number every different letter."""
    k = len(set(text))
    return len(text) * max(1, (k - 1).bit_length())


def entropy_bits(text: str) -> float:
    """Shannon's lower limit (Section 16.5): no code that spells each symbol separately can use fewer bits in total
    than the sum over symbols of count x log2(length / count). Huffman is always less than one bit per symbol above."""
    from math import log2
    n = len(text)
    return sum(c * log2(n / c) for c in Counter(text).values())


if __name__ == "__main__":
    print(round(entropy_bits(MESSAGE), 2), round(entropy_bits("A" * 50 + "B" * 20 + "C" * 20 + "D" * 10), 2))
    log = []
    codes = huffman_codes(MESSAGE, log)
    print(Counter(MESSAGE).most_common())
    print(log)
    print(sorted(codes.items(), key=lambda kv: (len(kv[1]), kv[0])))
    bits = encode(MESSAGE, codes)
    print(len(bits), fixed_bits(MESSAGE), decode(bits, codes) == MESSAGE)
