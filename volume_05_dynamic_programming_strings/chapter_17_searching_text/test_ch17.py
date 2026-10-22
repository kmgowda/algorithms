import random
import unittest

import ch17_examples as ex


class TestChapter17(unittest.TestCase):
    def test_newsletter(self) -> None:
        self.assertEqual(ex.naive_search(ex.NEWSLETTER, "club"), ([12, 38], 81))
        self.assertEqual((ex.naive_search(ex.NEWSLETTER, "poems"), ex.naive_search(ex.NEWSLETTER, "opera")), (([58], 79), ([], 77)))
        t = "a" * 1000
        self.assertEqual((ex.naive_search(t, "a" * 9 + "b")[1], ex.naive_search(t, "b" + "a" * 9)[1], len(ex.naive_search(t, "aaa")[0])), (9910, 991, 998))

    def test_every_case(self) -> None:
        self.assertEqual([ex.naive_search(t, p) for t, p in (("", "a"), ("abc", ""), ("ab", "abc"), ("abc", "abc"), ("aaaa", "aa"))],
                         [([], 0), ([0, 1, 2, 3], 0), ([], 0), ([0], 3), ([0, 1, 2], 6)])
        self.assertEqual((ex.naive_search(ex.NEWSLETTER, "the")[0], ex.naive_search("aab", "ab"), ex.naive_search("aaaaaa", "aab")[1]), ([0, 34, 67], ([1], 4), 12))
        r = random.Random(1)
        for _ in range(200):
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 20)))
            p = "".join(r.choice("ab") for _ in range(r.randint(1, 4)))
            self.assertEqual(ex.naive_search(t, p)[0], [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)])


    def test_shared_random_text(self) -> None:
        rt = ex.random_text()
        self.assertEqual((len(rt), ex.naive_search(rt, "library")), (10000, ([], 10350)))
        self.assertEqual((round(ex.expected_comparisons(10000, 7)), ex.expected_comparisons(3, 5)), (10378, 0.0))
        self.assertEqual(ex.naive_search("a" * 12, "aaab")[1], 36)
        self.assertEqual((ex.naive_search(rt, "reading club")[1], round(ex.expected_comparisons(10000, 12))), (10312, 10373))


if __name__ == "__main__":
    unittest.main()
