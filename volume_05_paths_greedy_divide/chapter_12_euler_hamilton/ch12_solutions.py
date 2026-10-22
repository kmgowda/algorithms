"""Volume 5, Chapter 12 - Thinking Problems: the shortest keypad sequence that tries every code (Thinking Problem 2,
an Euler circuit of one-way streets), and a map in one piece where every place has two roads but no route visits
every place (Thinking Problem 3).

Run:  python3 ch12_solutions.py
"""

from __future__ import annotations

import itertools

import ch12_examples as ex


def de_bruijn(k: int, n: int) -> str:
    """The shortest string of digits 0..k-1 that contains every n-digit code exactly once (Thinking Problem 2).
    Places are the (n-1)-digit strings; each n-digit code is a one-way street from its first n-1 digits to its last
    n-1. Every place has k streets out and k in, so an Euler circuit exists; Hierholzer's stack method finds it.
    Length k^n + n - 1. O(n k^n) work, counting the string slicing."""
    if k < 1 or n < 1:
        return ""
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"[:k]
    out = {"".join(p): list(reversed(digits)) for p in itertools.product(digits, repeat=n - 1)}
    start = digits[0] * (n - 1)
    stack, circuit = [(start, "")], []
    while stack:
        v, d = stack[-1]
        if out[v]:
            c = out[v].pop()                        # drive the street labelled v + c
            stack.append(((v + c)[1:], c))
        else:
            circuit.append(stack.pop()[1])
    return start + "".join(reversed(circuit))


def windmill(blades: int) -> tuple[list, list]:
    """A centre C and `blades` triangles C, a_i, b_i sharing only C: one piece, every place has at least 2 roads."""
    places = ["C"] + [f"{x}{i}" for i in range(1, blades + 1) for x in "ab"]
    roads = [r for i in range(1, blades + 1) for r in (("C", f"a{i}"), (f"a{i}", f"b{i}"), (f"b{i}", "C"))]
    return places, roads


if __name__ == "__main__":
    print(de_bruijn(2, 3), len(de_bruijn(10, 3)))
    for b in (1, 2, 3):
        places, roads = windmill(b)
        print(b, len(ex.hamiltonian_paths(places, roads)))
