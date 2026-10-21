import random
import unittest

import ch22_examples as ex


class TestChapter22(unittest.TestCase):
    def test_examples(self) -> None:
        goto, fail, out = ex.build(ex.WORDS)
        self.assertEqual((len(goto), fail, out[5]), (10, [0, 0, 0, 0, 1, 2, 0, 3, 0, 3], ["she", "he"]))
        self.assertEqual(ex.search("ushers", ex.WORDS), ([(1, "she"), (2, "he"), (2, "hers")], 7))
        post = "warning: spoiler ahead. in the ending the hero dies, the spoiler said"
        self.assertEqual(ex.search(post, ex.BANNED)[0], [(9, "spoiler"), (31, "ending"), (47, "dies"), (57, "spoiler")])

    def test_every_case(self) -> None:
        self.assertEqual((ex.search("", ex.WORDS)[0], ex.search("abc", [])[0], ex.search("xyz", ex.WORDS)[0]), ([], [], []))
        self.assertEqual(len(ex.search("aaaa", ["a", "aa", "aaa"])[0]), 9)
        self.assertEqual(ex.search("his hers", ex.WORDS)[0], [(0, "his"), (4, "he"), (4, "hers")])
        self.assertEqual(len(ex.search("ushers", ex.WORDS + ["her"])[0]), 4)
        self.assertEqual(ex.build(ex.WORDS)[1][7], 3)
        r = random.Random(22)
        for _ in range(300):
            words = list({"".join(r.choice("ab") for _ in range(r.randint(1, 4))) for _ in range(r.randint(1, 5))})
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 25)))
            found, steps = ex.search(t, words)
            self.assertEqual(found, ex.search_each(t, words))
            self.assertLessEqual(steps, 2 * len(t))


if __name__ == "__main__":
    unittest.main()
