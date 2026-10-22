import unittest

import ch24_examples as ex


class TestChapter64(unittest.TestCase):
    def test_every_case(self) -> None:
        r = ex.recommend
        rows = [({}, "array"), (dict(range_totals=True), "Fenwick tree"), (dict(range_totals=True, values_change=False), "prefix sums"),
                (dict(range_extremes=True), "segment tree"), (dict(range_extremes=True, values_change=False), "sparse table"),
                (dict(exact_keys=True), "hash table"), (dict(exact_keys=True, tiny_memory_ok_errors=True), "Bloom filter"),
                (dict(needs_order=True), "balanced search tree"), (dict(needs_order=True, on_disk=True), "B-tree"),
                (dict(tiny_memory_ok_errors=True), "array"), (dict(newest_first=True, oldest_first=True), "stack"),
                (dict(exact_keys=True, needs_order=True), "balanced search tree"), (dict(groups=True, extreme_only=True), "union-find"),
                (dict(prefixes=True, exact_keys=True), "trie")]
        for needs, want in rows:
            self.assertEqual(r(**needs), want)

    def test_library(self) -> None:
        got = {job: ex.recommend(**needs) for job, needs in ex.LIBRARY_JOBS.items()}
        self.assertEqual(got, {"catalogue by call number": "hash table", "subject browsing": "B-tree",
                               "title autocomplete": "trie", "help-desk requests": "binary heap",
                               "returns pile / undo": "stack", "waiting list": "queue",
                               "visitor dashboard": "Fenwick tree", "reading clubs": "union-find"})

    def test_exercises(self) -> None:
        self.assertEqual(ex.recommend(exact_keys=True, tiny_memory_ok_errors=True), "Bloom filter")
        self.assertEqual(ex.recommend(range_extremes=True, values_change=False), "sparse table")
        self.assertEqual(ex.recommend(needs_order=True), "balanced search tree")
        self.assertEqual(ex.recommend(groups=True), "union-find")


if __name__ == "__main__":
    unittest.main()
