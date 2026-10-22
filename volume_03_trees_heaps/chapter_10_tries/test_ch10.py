import random
import unittest

import ch10_examples as ex


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
        for word, result, nodes in (("map", True, 7), ("maps", True, 6), ("ma", False, 7)):   # delete cases
            d = ex.Trie()
            for w in ("map", "maps", "mat", "me"):
                d.insert(w)
            self.assertEqual((d.delete(word), ex.count_nodes(d)), (result, nodes))
        self.assertFalse(ex.Trie().delete("map"))
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

    def test_practice(self) -> None:
        t = ex.Trie()
        for w in "TEA TEN TO TOP TOY IN INN".split():
            t.insert(w)
        self.assertEqual(ex.count_nodes(t), 11)
        counts = []
        for w in ("TO", "TOP", "TEA", "TEN"):
            t.delete(w)
            counts.append(ex.count_nodes(t))
        self.assertEqual((counts, t.starting_with("T")), ([11, 10, 9, 7], ["TOY"]))

    def test_delete(self) -> None:
        t = ex.Trie()
        self.assertFalse(t.delete("CAT"))                                   # empty trie
        self.assertFalse(t.delete(""))
        for w in ["CAT", "CAR", "CART", "CARD", "DOG", "DOT"]:
            t.insert(w)
        steps = [("CAR", 11, ["CARD", "CART", "CAT"]),                     # unmark only: R still leads on
                 ("CART", 10, ["CARD", "CAT"]),                            # prune T
                 ("CARD", 8, ["CAT"])]                                     # prune D, then R
        for w, nodes, left in steps:
            self.assertTrue(t.delete(w))
            self.assertEqual((ex.count_nodes(t), t.starting_with("C")), (nodes, left))
        self.assertFalse(t.delete("CA"))                                    # a prefix, not a word
        self.assertFalse(t.delete("COW"))                                   # falls off the trie
        self.assertFalse(t.delete("CARD"))                                  # already gone
        for w in ["CAT", "DOG", "DOT"]:
            t.delete(w)
        self.assertEqual((ex.count_nodes(t), t.starting_with("")), (1, []))  # back to the bare root
        one = ex.Trie()
        one.insert("")
        self.assertEqual((one.delete(""), one.starting_with("")), (True, []))  # the empty word
        rng = random.Random(4)
        words = sorted({"".join(rng.choice("ab") for _ in range(rng.randint(1, 4))) for _ in range(30)})
        tt, ref = ex.Trie(), set(words)
        for w in words:
            tt.insert(w)
        for w in rng.sample(words, len(words) // 2):
            tt.delete(w)
            ref.discard(w)
            fresh = ex.Trie()
            for x in ref:
                fresh.insert(x)
            self.assertEqual((tt.starting_with(""), ex.count_nodes(tt)), (sorted(ref), ex.count_nodes(fresh)))


if __name__ == "__main__":
    unittest.main()
