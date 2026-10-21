import random
import unittest

import ch15_examples as ex


def is_subsequence(s: str, t: str) -> bool:
    it = iter(t)
    return all(ch in it for ch in s)


class TestChapter15(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.lcs_full("READING", "TRADING"), ex.lcs_two_rows("READING", "TRADING")), ((6, "RADING", 64), (6, 16)))
        self.assertEqual(ex.hirschberg("READING", "TRADING"), "RADING")
        r = random.Random(15)
        a = "".join(r.choice("ACGT") for _ in range(2000))
        b = "".join(r.choice("ACGT") for _ in range(2000))
        self.assertEqual((ex.lcs_two_rows(a, b), ex.lcs_full(a, b)[2]), ((1294, 4002), 4004001))

    def test_every_case(self) -> None:
        self.assertEqual((ex.lcs_two_rows("", "ABC"), ex.hirschberg("", "ABC"), ex.hirschberg("A", "XAY"), ex.hirschberg("ABC", "ABC")),
                         ((0, 8), "", "A", "ABC"))
        self.assertEqual(len(ex.hirschberg("ABC", "CBA")), 1)
        r = random.Random(3)
        for _ in range(200):
            a = "".join(r.choice("ABC") for _ in range(r.randint(0, 9)))
            b = "".join(r.choice("ABC") for _ in range(r.randint(0, 9)))
            h = ex.hirschberg(a, b)
            self.assertEqual(len(h), ex.lcs_full(a, b)[0])
            self.assertTrue(is_subsequence(h, a) and is_subsequence(h, b))


if __name__ == "__main__":
    unittest.main()
