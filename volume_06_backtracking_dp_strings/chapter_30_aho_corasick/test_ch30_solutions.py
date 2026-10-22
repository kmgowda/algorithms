import random
import unittest

import ch30_examples as ex
import ch30_solutions as sol


class TestChapter30Solutions(unittest.TestCase):
    def test_count_each(self) -> None:
        self.assertEqual(sol.count_each("", ["a"]), {"a": 0})
        self.assertEqual(sol.count_each("abc", []), {})
        self.assertEqual(sol.count_each("a", ["a"]), {"a": 1})
        self.assertEqual(sol.count_each("aaaa", ["a", "aa", "aaa"]), {"a": 4, "aa": 3, "aaa": 2})
        self.assertEqual(sol.count_each("ushers", ex.WORDS), {"he": 1, "she": 1, "his": 0, "hers": 1})
        r = random.Random(30)
        for _ in range(300):
            words = list({"".join(r.choice("ab") for _ in range(r.randint(1, 4))) for _ in range(r.randint(1, 5))})
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 25)))
            want = {w: sum(1 for _, x in ex.search_each(t, words) if x == w) for w in words}
            self.assertEqual(sol.count_each(t, words), want)

    def test_link_steps_bound(self) -> None:
        self.assertEqual((sol.link_steps([]), sol.link_steps(["a"]), sol.link_steps(ex.WORDS)), (0, 0, 0))
        self.assertEqual(sol.link_steps(["bbbbaaaa", "abaaa", "abbbaba"]), 12)
        r = random.Random(1)
        for _ in range(500):
            words = list({"".join(r.choice("ab") for _ in range(r.randint(1, 8))) for _ in range(r.randint(1, 6))})
            self.assertLessEqual(sol.link_steps(words), sum(map(len, words)) - len(words))

    def test_one_step_bug(self) -> None:
        self.assertEqual(sol.one_step_search("see", ["e", "see"]), [(0, "see"), (1, "e")])
        self.assertEqual(ex.search("see", ["e", "see"])[0], [(0, "see"), (1, "e"), (2, "e")])
        self.assertEqual(ex.links(["e", "see"])["see"], "e")


if __name__ == "__main__":
    unittest.main()
