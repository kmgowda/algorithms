import random
import unittest

import ch21_examples as ex


class TestChapter21(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.shift_table("club"), ex.shift_table("aaab")), ({"c": 3, "l": 2, "u": 1}, {"a": 1}))
        self.assertEqual((ex.horspool(ex.NEWSLETTER, "club"), ex.horspool(ex.NEWSLETTER, "library")), (([12, 38], 27, 20), ([71], 19, 13)))
        r = random.Random(21)
        t = "".join(r.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(10000))
        self.assertEqual([ex.horspool(t, p)[1:] for p in ("library", "reading club")], [(1648, 1573), (1097, 1054)])
        self.assertEqual((ex.horspool("a" * 1000, "a" * 9 + "b")[1:], ex.horspool("a" * 1000, "b" + "a" * 9)[1:]), ((991, 991), (9910, 991)))

    def test_every_case(self) -> None:
        self.assertEqual([ex.horspool(t, p) for t, p in (("", "a"), ("abc", ""), ("ab", "abc"), ("aaaa", "aa"), ("abc", "abc"))],
                         [([], 0, 0), ([0, 1, 2, 3], 0, 0), ([], 0, 0), ([0, 1, 2], 6, 3), ([0], 3, 1)])
        r = random.Random(1)
        for _ in range(300):
            t = "".join(r.choice("abc") for _ in range(r.randint(0, 30)))
            p = "".join(r.choice("abc") for _ in range(r.randint(1, 5)))
            self.assertEqual(ex.horspool(t, p)[0], [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)])


if __name__ == "__main__":
    unittest.main()
