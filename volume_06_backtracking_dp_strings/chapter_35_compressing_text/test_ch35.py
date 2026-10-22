import random
import unittest

import ch35_examples as ex


class TestChapter27(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.rle_encode("aaabccddddd"), ex.sizes("aaabccddddd")), ([("a", 3), ("b", 1), ("c", 2), ("d", 5)], (11, 8, 15)))
        self.assertEqual(ex.lz77_encode("abababab"), [(0, 0, "a"), (0, 0, "b"), (2, 5, "b")])
        self.assertEqual(ex.sizes(ex.POEM), (52, 102, 66))
        r = random.Random(27)
        rnd = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(300))
        self.assertEqual((ex.sizes(rnd), ex.sizes("a" * 300), ex.sizes("ab" * 150)), ((300, 572, 456), (300, 4, 9), (300, 600, 12)))

    def test_every_case(self) -> None:
        self.assertEqual((ex.rle_encode(""), ex.lz77_encode(""), ex.lz77_encode("a"), ex.lz77_encode("aaaa")), ([], [], [(0, 0, "a")], [(0, 0, "a"), (1, 2, "a")]))
        self.assertEqual(ex.sizes("abc"), (3, 6, 9))
        self.assertEqual((ex.rle_encode("wwwwbbw"), ex.lz77_decode([(0, 0, "x"), (1, 3, "y")]), ex.lz77_encode("ab" * 150)[2]), ([("w", 4), ("b", 2), ("w", 1)], "xxxxy", (2, 255, "b")))
        r = random.Random(1)
        for _ in range(300):
            s = "".join(r.choice("ab ") for _ in range(r.randint(0, 40)))
            self.assertEqual(ex.rle_decode(ex.rle_encode(s)), s)
            self.assertEqual(ex.lz77_decode(ex.lz77_encode(s)), s)


    def test_lzw_bwt_entropy(self) -> None:
        codes, d = ex.lzw_encode("abababab")
        self.assertEqual((codes, d), ([0, 1, 2, 4, 1], {"a": 0, "b": 1, "ab": 2, "ba": 3, "aba": 4, "abab": 5}))
        self.assertEqual(ex.lzw_decode(codes, ["a", "b"]), "abababab")
        self.assertEqual((ex.lzw_encode(""), ex.lzw_decode([], ["a"])), (([], {}), ""))
        self.assertEqual(ex.rle_encode("a" * 300), [("a", 255), ("a", 45)])
        self.assertEqual((ex.bwt("banana")[0], ex.bwt("abab")[0]), ("annb$aa", "bb$aa"))
        self.assertEqual(len(ex.lzw_encode(ex.POEM * 20)[0]), 226)
        self.assertEqual(ex.move_to_front("annb$aa"), [1, 3, 0, 3, 3, 3, 0])
        self.assertAlmostEqual(ex.entropy_bits("banana"), 8.7549, places=3)
        self.assertEqual((ex.entropy_bits(""), ex.entropy_bits("aaaa")), (0.0, 0.0))
        r = random.Random(27)
        for _ in range(300):
            t = "".join(r.choice("abc ") for _ in range(r.randint(0, 40)))
            c, _ = ex.lzw_encode(t)
            self.assertEqual(ex.lzw_decode(c, sorted(set(t))), t)
            self.assertEqual(ex.inverse_bwt(ex.bwt(t)[0]), t)
            self.assertEqual(ex.rle_decode(ex.rle_encode(t, longest=3)), t)


if __name__ == "__main__":
    unittest.main()
