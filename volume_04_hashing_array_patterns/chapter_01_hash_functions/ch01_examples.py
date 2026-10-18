"""Volume 4, Chapter 1 - The Magic Coat-Check: Hash Functions.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import hashlib
import os


def first_letter_hash(key: str, slots: int) -> int:
    """A BAD hash: only the first letter matters, so 'lion', 'lynx', 'llama' all collide."""
    return (ord(key[0].lower()) - ord("a")) % slots if key else 0


def sum_of_codes_hash(key: str, slots: int) -> int:
    """Still weak: anagrams like 'listen' and 'silent' always collide (order is ignored)."""
    return sum(ord(ch) for ch in key) % slots


def polynomial_hash(key: str, slots: int, base: int = 31) -> int:
    """A good everyday hash: h = c0*b^(n-1) + c1*b^(n-2) + ... computed with Horner's rule, mod slots."""
    h = 0
    for ch in key:
        h = (h * base + ord(ch)) % slots
    return h


def bucket_counts(keys: list[str], slots: int, hash_fn) -> list[int]:
    """How many keys land in each slot - a good hash spreads them evenly."""
    counts = [0] * slots
    for key in keys:
        counts[hash_fn(key, slots)] += 1
    return counts


def spread_report(keys: list[str], slots: int, hash_fn) -> dict[str, float]:
    """Summary: the fullest slot, empty slots, and the average keys per non-empty slot."""
    counts = bucket_counts(keys, slots, hash_fn)
    used = [c for c in counts if c]
    return {
        "max_in_one_slot": max(counts),
        "empty_slots": counts.count(0),
        "avg_per_used_slot": round(sum(used) / len(used), 2) if used else 0.0,
    }


def changed_bits(a: bytes, b: bytes) -> int:
    """How many bits differ between two equal-length byte strings."""
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def avalanche_demo(text_a: str, text_b: str) -> int:
    """A cryptographic hash changes about half its 256 bits when the input changes by one letter."""
    return changed_bits(hashlib.sha256(text_a.encode()).digest(), hashlib.sha256(text_b.encode()).digest())


def file_fingerprint(content: bytes) -> str:
    """Industry example: identical photos have identical SHA-256 fingerprints, so duplicates are found by hash."""
    return hashlib.sha256(content).hexdigest()


def find_duplicate_files(files: dict[str, bytes]) -> list[list[str]]:
    """Group file names whose contents are identical."""
    groups: dict[str, list[str]] = {}
    for name, content in files.items():
        groups.setdefault(file_fingerprint(content), []).append(name)
    return sorted(sorted(names) for names in groups.values() if len(names) > 1)


def hash_password(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """Industry example: store a slow, salted hash - never the password itself."""
    salt = salt if salt is not None else os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return salt, digest


def check_password(password: str, salt: bytes, stored: bytes) -> bool:
    return hash_password(password, salt)[1] == stored


ANIMALS = ["lion", "lynx", "llama", "lemur", "leopard", "zebra", "otter", "panda", "koala", "tiger",
           "listen", "silent", "enlist", "tinsel", "giraffe", "camel", "eagle", "hyena", "moose", "bison"]


if __name__ == "__main__":
    for name, fn in (("first letter", first_letter_hash), ("sum of codes", sum_of_codes_hash),
                     ("polynomial", polynomial_hash)):
        print(f"{name:>13}: {spread_report(ANIMALS, 13, fn)}")
    print("Python's own hash of 'lion' (changes between runs!):", hash("lion"))
    print("Bits changed by one letter (lion -> lioN):", avalanche_demo("lion", "lioN"), "of 256")
    photos = {"beach.jpg": b"\x01\x02sand", "beach_copy.jpg": b"\x01\x02sand", "zoo.jpg": b"\x09lion"}
    print("Duplicate files:", find_duplicate_files(photos))
    salt, stored = hash_password("correct horse battery staple")
    print("Password ok?", check_password("correct horse battery staple", salt, stored),
          "| wrong one?", check_password("password123", salt, stored))
