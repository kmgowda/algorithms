"""Volume 7, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

from ch11_examples import choose


def pick_for_scenarios() -> dict[str, str]:
    """Exercise 1: match real scenarios to structures."""
    return {
        "hospital triage board": choose("next most urgent item"),
        "stock price: highest price in any past window": choose("range min/max on static data"),
        "game: total gold in a region of tiles that change": choose("range sums with point updates"),
        "social network: are two users in the same community as friendships form": choose("are these connected, as links are added"),
        "URL shortener: has this short code ever been used?": choose("seen before, with tiny memory"),
    }


def memory_estimate(n: int) -> dict[str, int]:
    """Exercise 2: rough slot counts for n items."""
    return {"binary heap": n, "Fenwick tree": n + 1, "segment tree (recursive)": 4 * n,
            "segment tree (iterative)": 2 * n, "sparse table": n * max(1, n.bit_length())}


if __name__ == "__main__":
    print(pick_for_scenarios())
    print(memory_estimate(1024))
