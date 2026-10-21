import random
import unittest

import ch21_examples as ex


class TestChapter50(unittest.TestCase):
    def test_trie(self) -> None:
        t = ex.Trie()
        for w in ["CAT", "CAR", "CART", "CARD", "DOG", "DOT"]:
            t.insert(w)
        self.assertEqual(t.starting_with("CAR"), ["CAR", "CARD", "CART"])
        self.assertEqual(t.starting_with("CO"), [])
        self.assertEqual(ex.count_nodes(t), 11)
        t.insert("CA")
        self.assertEqual(ex.count_nodes(t), 11)
        rng = random.Random(1)
        words = {"".join(rng.choice("abc") for _ in range(rng.randint(1, 5))) for _ in range(200)}
        tt = ex.Trie()
        for w in words:
            tt.insert(w)
        for p in ["", "a", "ab", "cab", "ccc"]:
            self.assertEqual(tt.starting_with(p), sorted(w for w in words if w.startswith(p)))


if __name__ == "__main__":
    unittest.main()
