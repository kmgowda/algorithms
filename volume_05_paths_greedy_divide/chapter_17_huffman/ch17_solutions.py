"""Volume 5, Chapter 17 - Thinking Problems.

Problem 1: Huffman code lengths satisfy sum 2^(-length) = 1 exactly (a full code tree), checked on many texts.
Problem 2: with counts already sorted, Huffman in O(n) using two queues instead of a heap; same total bits.
Problem 3: a code that is not prefix-free (A=0, B=01, C=1) cannot be decoded: '01' reads as B or as AC.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction

from ch17_examples import encode, huffman_codes


def kraft_sum(codes: dict) -> Fraction:
    return sum((Fraction(1, 2 ** len(c)) for c in codes.values()), Fraction(0))


def two_queue_total_bits(sorted_counts: list) -> int:
    """Total encoded length from counts sorted smallest first: leaves in one queue, joined groups in another."""
    if len(sorted_counts) <= 1:
        return sum(sorted_counts)                     # one symbol: one bit each
    leaves, joined, total = deque(sorted_counts), deque(), 0

    def smallest():
        if not joined or (leaves and leaves[0] <= joined[0]):
            return leaves.popleft()
        return joined.popleft()
    while len(leaves) + len(joined) > 1:
        s = smallest() + smallest()
        total += s                                     # each join adds one bit to every symbol below it
        joined.append(s)                               # joined sums come out in increasing order
    return total


def all_parses(bits: str, codes: dict) -> list:
    """Every way to split bits into code words."""
    if not bits:
        return [""]
    out = []
    for ch, c in codes.items():
        if bits.startswith(c):
            out += [ch + rest for rest in all_parses(bits[len(c):], codes)]
    return out


BAD_CODE = {"A": "0", "B": "01", "C": "1"}


if __name__ == "__main__":
    from ch17_examples import MESSAGE
    codes = huffman_codes(MESSAGE)
    print(kraft_sum(codes), len(encode(MESSAGE, codes)), two_queue_total_bits(sorted(Counter(MESSAGE).values())))
    print(all_parses("01", BAD_CODE), all_parses("0110", BAD_CODE))
