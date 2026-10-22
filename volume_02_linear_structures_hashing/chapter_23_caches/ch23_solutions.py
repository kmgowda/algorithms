"""Volume 2, Chapter 23 - Thinking Problem solutions (Section 23.14)."""

from __future__ import annotations

from collections import OrderedDict

import ch23_examples as ex


def width_lru_hits(requests, widths: dict, room: float) -> tuple[int, list]:
    """Thinking Problem 23.2: LRU on a shelf of a given width, books of different widths.

    On a miss, return least recently used books until the new one fits; a book wider than the shelf is never
    shelved. Amortized O(1) per request. Returns (hits, final shelf oldest first)."""
    shelf: OrderedDict = OrderedDict()             # a map plus a doubly linked list, oldest use first
    used = hits = 0
    for r in requests:
        if r in shelf:
            hits += 1
            shelf.move_to_end(r)                   # now the most recent
            continue
        if widths[r] > room:
            continue                               # can never fit: fetch it, do not shelve it
        while used + widths[r] > room:             # each book is evicted at most once per arrival
            old, w = shelf.popitem(last=False)
            used -= w
        shelf[r] = widths[r]
        used += widths[r]
    return hits, list(shelf)


class EvictFirstLRU(ex.LRUCache):
    """Thinking Problem 23.3: the buggy put that makes room before checking whether the key is already there."""

    def put(self, key, value) -> None:
        if len(self.map) == self.capacity:
            oldest = self.head.next
            self._unlink(oldest)
            del self.map[oldest.key]
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._unlink(node)
            self._append(node)
            return
        node = ex._Node(key, value)
        self._append(node)
        self.map[key] = node


def fifo_hits_by_size(requests, sizes) -> list[int]:
    """Thinking Problem 23.1: FIFO hits for each shelf size (Belady's anomaly shows up here)."""
    return [ex.count_hits(requests, k, "fifo") for k in sizes]
