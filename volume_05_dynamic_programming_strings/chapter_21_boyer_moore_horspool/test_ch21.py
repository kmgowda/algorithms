import random
import unittest

import ch21_examples as ex


class TestChapter21(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.shift_table("club"), ex.shift_table("aaab")), ({"c": 3, "l": 2, "u": 1}, {"a": 1}))
        self.assertEqual((ex.horspool(ex.NEWSLETTER, "club"), ex.horspool(ex.NEWSLETTER, "library")), (([12, 38], 27, 20), ([71], 19, 13)))
        t = ex.random_text()
        self.assertEqual([ex.horspool(t, p)[1:] for p in ("library", "reading club")], [(1624, 1559), (1086, 1046)])
        self.assertEqual((ex.horspool("a" * 1000, "a" * 9 + "b")[1:], ex.horspool("a" * 1000, "b" + "a" * 9)[1:]), ((991, 991), (9910, 991)))

    def test_every_case(self) -> None:
        self.assertEqual([ex.horspool(t, p) for t, p in (("", "a"), ("abc", ""), ("ab", "abc"), ("aaaa", "aa"), ("abc", "abc"))],
                         [([], 0, 0), ([0, 1, 2, 3], 0, 0), ([], 0, 0), ([0, 1, 2], 6, 3), ([0], 3, 1)])
        r = random.Random(1)
        for _ in range(300):
            t = "".join(r.choice("abc") for _ in range(r.randint(0, 30)))
            p = "".join(r.choice("abc") for _ in range(r.randint(1, 5)))
            self.assertEqual(ex.horspool(t, p)[0], [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)])


    def test_good_suffix(self) -> None:
        self.assertEqual(ex.good_suffix_table("baaaaaaaaa"), [10, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(ex.good_suffix_table("abacab"), [4, 4, 4, 4, 4, 6, 1])
        a = "a" * 1000
        self.assertEqual((ex.boyer_moore(a, "b" + "a" * 9)[1:], ex.boyer_moore(a, "a" * 9 + "b")[1:], ex.boyer_moore(a, "aaa")[1:]),
                         ((1000, 100), (991, 991), (2994, 998)))
        self.assertEqual(ex.boyer_moore(ex.NEWSLETTER, "club"), ([12, 38], 27, 20))
        self.assertEqual([ex.boyer_moore(t, p) for t, p in (("", "a"), ("abc", ""), ("ab", "abc"), ("aaaa", "aa"))],
                         [([], 0, 0), ([0, 1, 2, 3], 0, 0), ([], 0, 0), ([0, 1, 2], 6, 3)])
        self.assertEqual(ex.good_suffix_table("a"), [1, 1])
        r = random.Random(21)
        for _ in range(500):
            t = "".join(r.choice("abc") for _ in range(r.randint(0, 40)))
            p = "".join(r.choice("abc") for _ in range(r.randint(1, 6)))
            self.assertEqual(ex.boyer_moore(t, p)[0], [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)])


if __name__ == "__main__":
    unittest.main()
