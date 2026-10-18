import random
import unittest
from collections import Counter

import ch03_examples as ex
import ch03_solutions as sol


class TestExamples(unittest.TestCase):
    def test_top_k(self) -> None:
        story = "The lion saw the zebra. The zebra ran. The lion slept."
        self.assertEqual(ex.top_k_words(story, 3), [("the", 4), ("lion", 2), ("zebra", 2)])
        self.assertEqual(ex.top_k_words("", 3), [])

    def test_group_and_dedupe(self) -> None:
        patients = [{"name": "Ana", "ward": "A"}, {"name": "Ben", "ward": "B"}, {"name": "Cy", "ward": "A"}]
        self.assertEqual(ex.group_by(patients, "ward"), {"A": ["Ana", "Cy"], "B": ["Ben"]})
        rng = random.Random(1)
        for _ in range(200):
            items = [rng.choice("abcde") for _ in range(rng.randint(0, 12))]
            self.assertEqual(ex.dedupe_keep_order(items), list(dict.fromkeys(items)))

    def test_reconcile(self) -> None:
        self.assertEqual(ex.reconcile(["P1", "P2", "P3"], ["P2", "P3", "P4"]),
                         {"only_in_warehouse": ["P1"], "only_on_website": ["P4"], "in_both": ["P2", "P3"]})

    def test_index(self) -> None:
        idx = ex.inverted_index({"d1": "Lions live in Africa.", "d2": "Lions and tigers.", "d3": "Tigers live in Asia."})
        self.assertEqual(ex.search_all(idx, "lions live"), {"d1"})
        self.assertEqual(ex.search_all(idx, "live"), {"d1", "d3"})
        self.assertEqual(ex.search_all(idx, "penguins"), set())
        self.assertEqual(ex.search_all(idx, ""), set())

    def test_anagrams(self) -> None:
        self.assertEqual(ex.anagram_buckets(["listen", "silent", "enlist", "lion", "loin", "zebra"]),
                         [["enlist", "listen", "silent"], ["lion", "loin"], ["zebra"]])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertTrue(sol.is_ransom_note_possible("zoo", "oozebra"))
        self.assertFalse(sol.is_ransom_note_possible("zoo", "zebra"))
        rng = random.Random(2)
        for _ in range(200):
            a = [rng.randint(0, 5) for _ in range(rng.randint(0, 10))]
            b = [rng.randint(0, 5) for _ in range(rng.randint(0, 10))]
            expected = sorted(x for x in set(a) for _ in range(min(a.count(x), b.count(x))))
            self.assertEqual(sol.intersection_with_counts(a, b), expected)
        self.assertEqual(sol.first_seen_day([(1, "Ana"), (2, "Ben"), (3, "Ana")]), {"Ana": 1, "Ben": 2})
        self.assertEqual(sol.friends_in_common({"A": {"x", "y"}, "B": {"y", "z"}, "C": {"x", "y", "z"}}),
                         {("A", "B"): 1, ("A", "C"): 2, ("B", "C"): 2})
        self.assertEqual(sol.tags_to_items({"pancakes": ["egg", "milk"], "omelette": ["egg"]}),
                         {"egg": ["omelette", "pancakes"], "milk": ["pancakes"]})
        self.assertEqual(Counter("aab")["a"], 2)


if __name__ == "__main__":
    unittest.main()
