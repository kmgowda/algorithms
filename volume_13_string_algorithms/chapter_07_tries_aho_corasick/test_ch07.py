import os
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


def naive_multi(text, patterns):
    return sorted((i, p) for p in set(patterns) for i in range(len(text) - len(p) + 1) if text[i:i + len(p)] == p)


class TestAhoCorasick(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            pats = list({"".join(rng.choice("ab") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(1, 6))})
            text = "".join(rng.choice("ab") for _ in range(rng.randint(0, 30)))
            self.assertEqual(ex.AhoCorasick(pats).search(text), naive_multi(text, pats))
            t = ex.Trie()
            for p in pats:
                t.add(p)
            pre = "".join(rng.choice("ab") for _ in range(rng.randint(0, 2)))
            self.assertEqual(t.starts_with(pre), sorted(p for p in pats if p.startswith(pre)))
            self.assertEqual(sol.longest_common_prefix(pats), os.path.commonprefix(pats))

    def test_examples(self) -> None:
        self.assertEqual(ex.AhoCorasick(["he", "she", "his", "hers"]).search("ushers"), [(1, "she"), (2, "he"), (2, "hers")])
        self.assertEqual(ex.mask_banned_words("That darn spam is SPAMMY", ["darn", "spam"]), "That **** **** is ****MY")
        self.assertEqual(sol.count_each_pattern("ACGTACGTAC", ["ACG", "GTA", "TT"]), {"ACG": 2, "GTA": 2, "TT": 0})
        self.assertEqual(sol.replace_with_roots("the cattle was rattled by the battery", ["cat", "bat", "rat"]),
                         "the cat was rat by the bat")


if __name__ == "__main__":
    unittest.main()
