"""Volume 2, Chapter 11 - Amortized Analysis: Why Appending to a List Is Cheap on Average.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import sys


# ------------------------------------------------------------------ a simulated dynamic array
def simulate_appends(n: int, grow: str = "double", initial_capacity: int = 1, step: int = 10) -> dict[str, int]:
    """Append n items to a pretend array that must copy everything when it runs out of room.

    grow = "double": new capacity = 2 x old capacity
    grow = "add":    new capacity = old capacity + step
    Returns total copies, the most expensive single append, number of resizes, final capacity.
    """
    capacity, size = initial_capacity, 0
    copies = resizes = worst_single = 0
    for _ in range(n):
        cost = 1                                   # writing the new item
        if size == capacity:
            cost += size                           # copy every existing item to the new block
            copies += size
            resizes += 1
            capacity = capacity * 2 if grow == "double" else capacity + step
        size += 1
        worst_single = max(worst_single, cost)
    return {"copies": copies, "worst_single_append": worst_single, "resizes": resizes, "capacity": capacity}


def amortized_cost_per_append(n: int, grow: str = "double") -> float:
    """(writes + copies) / appends: the average cost per append over the whole sequence."""
    stats = simulate_appends(n, grow)
    return (n + stats["copies"]) / n


def accounting_bank_never_negative(n: int, charge: int = 3) -> bool:
    """Accounting method: charge every append `charge` coins; pay 1 per write and 1 per copy.

    With doubling, a charge of 3 keeps the savings from ever going negative.
    """
    capacity, size, bank = 1, 0, 0
    for _ in range(n):
        bank += charge
        if size == capacity:
            bank -= size                           # pay for copying
            capacity *= 2
        bank -= 1                                  # pay for the write
        size += 1
        if bank < 0:
            return False
    return True


# ------------------------------------------------------------------ the real Python list
def python_list_resize_points(n: int) -> list[int]:
    """Sizes at which CPython's list grew its memory block while appending n items."""
    points = []
    items: list[int] = []
    last = sys.getsizeof(items)
    for i in range(n):
        items.append(i)
        size_now = sys.getsizeof(items)
        if size_now != last:
            points.append(len(items))
            last = size_now
    return points


# ------------------------------------------------------------------ binary counter
def increment_flips(bits: list[int]) -> int:
    """Add 1 to a little-endian list of bits (bits[0] is the lowest). Returns how many bits flipped."""
    flips = 0
    i = 0
    while i < len(bits) and bits[i] == 1:
        bits[i] = 0
        flips += 1
        i += 1
    if i == len(bits):
        bits.append(1)
    else:
        bits[i] = 1
    return flips + 1


def total_flips_counting_to(n: int) -> tuple[int, int]:
    """(total flips, worst single increment) while counting from 0 to n."""
    bits: list[int] = []
    total = worst = 0
    for _ in range(n):
        flips = increment_flips(bits)
        total += flips
        worst = max(worst, flips)
    return total, worst


# ------------------------------------------------------------------ industry: write buffering
def buffered_writes(records: int, buffer_size: int, flush_cost: int = 100) -> tuple[float, int]:
    """Industry example: a database collects writes in memory and flushes them to disk in batches.

    Each record costs 1 to add; each flush costs `flush_cost` (one slow disk operation).
    Returns (amortized cost per record, worst single write).
    """
    total = worst = 0
    pending = 0
    for _ in range(records):
        cost = 1
        pending += 1
        if pending == buffer_size:
            cost += flush_cost
            pending = 0
        total += cost
        worst = max(worst, cost)
    return total / records, worst


if __name__ == "__main__":
    for grow in ("double", "add"):
        stats = simulate_appends(100_000, grow)
        print(f"{grow:>6}: {stats} | amortized cost per append = {amortized_cost_per_append(100_000, grow):.2f}")
    print("Accounting with 3 coins works:", accounting_bank_never_negative(1_000_000),
          "| with 2 coins:", accounting_bank_never_negative(1_000_000, charge=2))
    print("CPython list grew at sizes:", python_list_resize_points(100))
    print("Counting to 1,000,000 - (total flips, worst single):", total_flips_counting_to(1_000_000))
    print("Buffered writes (amortized, worst):", buffered_writes(10_000, buffer_size=500))
