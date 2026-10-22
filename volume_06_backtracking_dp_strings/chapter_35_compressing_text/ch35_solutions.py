"""Volume 6, Chapter 35 - Thinking Problems.

Problem 1: run-length decoding undoes encoding for every text, with at most one pair per letter (checked).
Problem 2: transform, then compress: the Burrows-Wheeler transform gathers equal letters into runs.
Problem 3: copying an LZ77 match as one slice breaks overlapping copies such as (2, 5, 'b') in abababab.
"""

from __future__ import annotations

from ch35_examples import bwt, lz77_encode, rle_decode, rle_encode


def runs_after_bwt(s: str) -> tuple[int, int]:
    """(runs in s, runs in its Burrows-Wheeler transform)."""
    return len(rle_encode(s)), len(rle_encode(bwt(s)[0]))


def lz77_decode_slice(triples: list) -> str:
    out = ""
    for dist, length, ch in triples:
        start = len(out) - dist
        out += out[start:start + length] + ch          # the bug: the slice cannot see letters it is still producing
    return out


if __name__ == "__main__":
    from ch35_examples import POEM
    print(runs_after_bwt(POEM), runs_after_bwt("banana"), lz77_decode_slice(lz77_encode("abababab")))
    print(rle_decode(rle_encode("aaab")))
