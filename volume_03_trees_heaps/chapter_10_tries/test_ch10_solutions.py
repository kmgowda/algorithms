import random
import unittest

import ch10_solutions as sol
from ch10_examples import Trie, count_nodes


def trie_of(words):
    t = Trie()
    for w in words:
        t.insert(w)
    return t


class TestChapter10Solutions(unittest.TestCase):
    def test_node_formula(self) -> None:
        for words in ([], [""], ["A"], ["CAT", "CAR", "CART", "CARD", "DOG", "DOT"], ["map", "maps", "mat", "me"],
                      ["ab", "ab", "abc"]):
            self.assertEqual(sol.nodes_by_formula(words), count_nodes(trie_of(words)))
        rng = random.Random(2)
        for _ in range(300):
            words = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 25))]
            self.assertEqual(sol.nodes_by_formula(words), count_nodes(trie_of(words)))

    def test_shortest_unique_prefixes(self) -> None:
        self.assertEqual(sol.shortest_unique_prefixes([]), {})
        self.assertEqual(sol.shortest_unique_prefixes(["ATLAS"]), {"ATLAS": "A"})
        self.assertEqual(sol.shortest_unique_prefixes([""]), {"": ""})
        self.assertEqual(sol.shortest_unique_prefixes(["CAR", "CAR"]), {"CAR": "C"})       # a duplicate
        self.assertEqual(sol.shortest_unique_prefixes(["CAR", "CART"]), {"CAR": "CAR", "CART": "CART"})
        self.assertEqual(sol.shortest_unique_prefixes(["ATLAS", "BIRDS", "BIOLOGY", "CHESS", "CHEMISTRY", "COOKING"]),
                         {"ATLAS": "A", "BIRDS": "BIR", "BIOLOGY": "BIO", "CHESS": "CHES", "CHEMISTRY": "CHEM",
                          "COOKING": "CO"})
        rng = random.Random(6)
        for _ in range(300):
            words = list({"".join(rng.choice("ab") for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(1, 12))})
            got = sol.shortest_unique_prefixes(words)
            for w in words:
                p = got[w]
                others = [v for v in words if v != w]
                unique = lambda q: not any(v.startswith(q) for v in others)  # noqa: E731
                if unique(p):
                    self.assertFalse(any(unique(w[:k]) for k in range(1, len(p))))   # shortest
                else:
                    self.assertEqual(p, w)
                    self.assertFalse(any(unique(w[:k]) for k in range(1, len(w) + 1)))

    def test_branch_only_delete_loses_words(self) -> None:
        t = trie_of(["CAR", "CART", "CAT"])
        self.assertTrue(sol.delete_branch_only(t, "CART"))
        self.assertEqual(t.starting_with(""), [])                    # CAR and CAT have gone as well
        t = trie_of(["CAR", "CART", "CAT"])
        t.delete("CART")
        self.assertEqual(t.starting_with(""), ["CAR", "CAT"])
        self.assertFalse(sol.delete_branch_only(Trie(), "CAR"))      # empty trie


if __name__ == "__main__":
    unittest.main()
