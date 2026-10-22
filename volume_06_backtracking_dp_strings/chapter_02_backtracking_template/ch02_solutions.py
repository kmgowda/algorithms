"""Volume 6, Chapter 2 - model solutions to the Thinking Problems (Section 2.14)."""

from __future__ import annotations

from ch02_examples import clash


def round_seatings(readers: list, feuds: list) -> list:
    """Every seating around a round table (seat n is beside seat 1) with no feuding neighbours, each rotation
    once: the first reader is fixed, each new reader is checked against the last one, and the last seat is
    also checked against the first. O(1) feud checks per choice."""
    if not readers:
        return [[]]
    out, row = [], [readers[0]]

    def go():
        if len(row) == len(readers):
            if len(row) < 3 or not clash(row[-1], row[0], feuds):
                out.append(list(row))
            return
        for r in readers:
            if r in row or clash(row[-1], r, feuds):
                continue
            row.append(r)
            go()
            row.pop()

    go()
    return out


def too_strict(readers: list, feuds: list) -> list:
    """Thinking Problem 3's buggy check: refuse a reader who feuds with ANYONE already seated."""
    out, row = [], []

    def go():
        if len(row) == len(readers):
            out.append(list(row))
            return
        for r in readers:
            if r not in row and not any(clash(s, r, feuds) for s in row):
                row.append(r)
                go()
                row.pop()

    go()
    return out
