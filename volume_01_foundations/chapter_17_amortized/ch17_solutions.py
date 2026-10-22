"""Volume 1, Chapter 17, Thinking Problem 2 - a visitor counter that can also be reset.

The door counter of Section 17.5 gains a Reset button that the librarian presses at closing time. Reset only clears
the lamps up to the highest lamp that is on, so any mix of n increments and resets costs O(n) lamp visits.

Run:  python3 ch17_solutions.py
"""

from __future__ import annotations


def run_counter(operations: list[str], bits: int = 8) -> tuple[list[int], list[int]]:
    """Apply "inc" / "reset" operations to a counter that starts at 0.

    Returns (final lamps, lowest lamp first; lamps visited by each operation). Reset visits lamps 0..high only,
    where high is the highest lamp that is on (-1 when every lamp is off)."""
    lamps, high, costs = [0] * bits, -1, []
    for op in operations:
        if op == "inc":
            k = 0
            while k < bits and lamps[k] == 1:
                lamps[k] = 0
                k += 1
            if k < bits:
                lamps[k] = 1
                high = max(high, k)
                costs.append(k + 1)
            else:
                high = -1
                costs.append(k)
        else:
            for k in range(high + 1):
                lamps[k] = 0
            costs.append(high + 1)
            high = -1
    return lamps, costs


if __name__ == "__main__":
    lamps, costs = run_counter(["inc"] * 13 + ["reset"] + ["inc"] * 3 + ["reset"])
    print(lamps, costs, sum(costs))
