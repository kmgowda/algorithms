import unittest

import ch64_examples as ex


class TestChapter64(unittest.TestCase):
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
