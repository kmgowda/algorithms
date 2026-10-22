"""Volume 2, Chapter 13 - Thinking Problems.

Problem 2: delete from a linear-probing table without tombstones, by shifting keys back into the hole.
A table is a list of keys, with None for an empty slot; every key's home is hash(key) % len(slots).
"""

from __future__ import annotations


def lp_find(slots: list, key) -> int:
    """The slot holding key under linear probing, or -1 if it is absent."""
    m = len(slots)
    i = hash(key) % m
    for _ in range(m):
        if slots[i] is None:
            return -1
        if slots[i] == key:
            return i
        i = (i + 1) % m
    return -1


def lp_insert(slots: list, key) -> None:
    """Put key in the first empty slot from its home (the table must have an empty slot)."""
    m = len(slots)
    i = hash(key) % m
    while slots[i] is not None and slots[i] != key:
        i = (i + 1) % m
    slots[i] = key


def backward_shift_delete(slots: list, key) -> bool:
    m = len(slots)
    i = lp_find(slots, key)
    if i < 0:
        return False
    slots[i] = None                          # open a hole
    j = i
    while True:
        j = (j + 1) % m
        if slots[j] is None:                 # the run has ended
            return True
        k = hash(slots[j]) % m               # home of the key in slot j
        if (i <= j and (k <= i or k > j)) or (i > j and j < k <= i):
            slots[i], slots[j] = slots[j], None   # its walk crossed the hole
            i = j


if __name__ == "__main__":
    t = [None] * 8
    for key in (7, 15, 1, 9):
        lp_insert(t, key)
    print(t)
    backward_shift_delete(t, 7)
    print(t, lp_find(t, 15))
