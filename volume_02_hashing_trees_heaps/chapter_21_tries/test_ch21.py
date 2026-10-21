import random
import unittest

import ch21_examples as ex


class TestChapter50(unittest.TestCase):
    def test_every_case(self) -> None:
        t = ex.Trie()
        self.assertEqual((t.starting_with("a"), ex.count_nodes(t)), ([], 1))
        for w in ("map", "maps", "mat", "me"):
            t.insert(w)
        self.assertEqual([t.starting_with(p) for p in ("ma", "map", "maps", "mapsx", "z", "")],
                         [["map", "maps", "mat"], ["map", "maps"], ["maps"], [], [], ["map", "maps", "mat", "me"]])
        self.assertEqual(ex.count_nodes(t), 7)
        t.insert("map")
        self.assertEqual(ex.count_nodes(t), 7)
        t.insert("")
        self.assertEqual(t.starting_with("")[0], "")
        c = ex.Trie()
        c.insert("Map")
        self.assertEqual((c.starting_with("ma"), c.starting_with("Ma")), ([], ["Map"]))

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
