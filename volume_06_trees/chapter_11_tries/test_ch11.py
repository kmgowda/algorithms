import random
import string
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestTrie(unittest.TestCase):
    def test_against_model(self) -> None:
        rng = random.Random(1)
        t, words = ex.Trie(), set()
        for _ in range(2000):
            w = "".join(rng.choice("abc") for _ in range(rng.randint(1, 5)))
            if rng.random() < 0.7:
                if w not in words:
                    t.insert(w)
                    words.add(w)
            else:
                self.assertEqual(t.delete(w), w in words)
                words.discard(w)
            p = "".join(rng.choice("abc") for _ in range(rng.randint(0, 3)))
            self.assertEqual(t.count_prefix(p), sum(1 for x in words if x.startswith(p)))
        for p in ["", "a", "ab", "cab"]:
            self.assertEqual(t.words_with_prefix(p), sorted(x for x in words if x.startswith(p)))
            self.assertEqual(t.starts_with(p), any(x.startswith(p) for x in words) or p == "")
        for w in list(words)[:50]:
            self.assertTrue(t.contains(w))

    def test_suggest_and_lcp(self) -> None:
        t = ex.Trie()
        for word, pop in [("lion", 90), ("lioness", 40), ("lime", 70), ("limo", 10), ("zebra", 80)]:
            t.insert(word, pop)
        self.assertEqual(t.suggest("li"), ["lion", "lime", "lioness"])
        self.assertEqual(t.suggest("q"), [])
        self.assertEqual(ex.longest_common_prefix(["flower", "flow", "flight"]), "fl")
        self.assertEqual(ex.longest_common_prefix(["dog", "dogs"]), "dog")
        self.assertEqual(ex.longest_common_prefix([]), "")


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        t = ex.Trie()
        for w in ("bad", "dad", "mad"):
            t.insert(w)
        self.assertTrue(sol.search_with_wildcard(t, ".ad"))
        self.assertTrue(sol.search_with_wildcard(t, "b.."))
        self.assertFalse(sol.search_with_wildcard(t, "b."))
        self.assertEqual(sol.replace_with_roots(["cat", "bat", "rat"], "the cattle was rattled by the battery"),
                         "the cat was rat by the bat")
        rng = random.Random(2)
        for _ in range(50):
            s = "".join(rng.choice(string.ascii_lowercase[:3]) for _ in range(rng.randint(0, 8)))
            self.assertEqual(sol.count_distinct_substrings(s), len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)}))
        self.assertEqual(sol.phone_contacts_matching(["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mou"),
                         ["mobile, moneypot, monitor", "mobile, moneypot, monitor", "mouse, mousepad"])


if __name__ == "__main__":
    unittest.main()
