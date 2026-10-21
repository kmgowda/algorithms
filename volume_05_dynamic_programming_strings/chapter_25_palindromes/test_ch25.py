import random
import unittest

import ch25_examples as ex


class TestChapter25(unittest.TestCase):
    def test_examples(self) -> None:
        got = [(ex.expand_around_centres(w), ex.manacher(w)[::2]) for w in ("level", "abacabad", "noon", "racecar drive")]
        self.assertEqual(got, [(("level", 13), ("level", 13)), (("abacaba", 24), ("abacaba", 23)), (("noon", 10), ("noon", 10)),
                               (("racecar", 38), ("racecar", 38))])
        self.assertEqual((ex.expand_around_centres("a" * 1000)[1], ex.manacher("a" * 1000)[2]), (500500, 1999))
        self.assertEqual(ex.manacher("abacabad")[1][7], 7)

    def test_every_case(self) -> None:
        self.assertEqual((ex.manacher("")[0], ex.manacher("a")[0], ex.manacher("ab")[0], ex.expand_around_centres("")[0]), ("", "a", "a", ""))
        self.assertEqual(ex.manacher("abba is a band")[0], "abba")
        r = random.Random(25)
        for _ in range(300):
            s = "".join(r.choice("ab") for _ in range(r.randint(0, 20)))
            best = max((s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1]), key=len, default="")
            self.assertEqual(len(ex.manacher(s)[0]), len(best))
            self.assertEqual(len(ex.expand_around_centres(s)[0]), len(best))
            self.assertLessEqual(ex.manacher(s)[2], 2 * (2 * len(s) + 1))


if __name__ == "__main__":
    unittest.main()
