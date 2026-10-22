import random
import unittest

import ch29_examples as ex
import ch29_solutions as sol


def plain(t, p):
    return [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]


class TestThinkingProblems(unittest.TestCase):
    def test_never_skips(self) -> None:
        r = random.Random(29)
        for _ in range(300):
            t = "".join(r.choice("abc") for _ in range(r.randint(0, 40)))
            p = "".join(r.choice("abc") for _ in range(r.randint(1, 5)))
            self.assertEqual(ex.horspool(t, p)[0], plain(t, p))
            self.assertEqual(sol.sunday(t, p)[0], plain(t, p))

    def test_sunday_on_newsletter(self) -> None:
        self.assertEqual(sol.sunday(ex.NEWSLETTER, "library"), ([71], 11))
        self.assertEqual(ex.horspool(ex.NEWSLETTER, "library")[2], 13)

    def test_whole_table_stalls(self) -> None:
        self.assertEqual(sol.horspool_whole_table("the club", "club"), ([4], 1000))
        self.assertEqual(sol.horspool_whole_table("xbab", "ab"), ([], 1000))


if __name__ == "__main__":
    unittest.main()
