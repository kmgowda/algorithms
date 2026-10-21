import random
import unittest

import ch27_examples as ex


class TestChapter27(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.rle_encode("aaabccddddd"), ex.sizes("aaabccddddd")), ([("a", 3), ("b", 1), ("c", 2), ("d", 5)], (11, 8, 15)))
        self.assertEqual(ex.lz77_encode("abababab"), [(0, 0, "a"), (0, 0, "b"), (2, 5, "b")])
        self.assertEqual(ex.sizes(ex.POEM), (52, 102, 66))
        r = random.Random(27)
        rnd = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(300))
        self.assertEqual((ex.sizes(rnd), ex.sizes("a" * 300), ex.sizes("ab" * 150)), ((300, 572, 456), (300, 2, 6), (300, 600, 9)))

    def test_every_case(self) -> None:
        self.assertEqual((ex.rle_encode(""), ex.lz77_encode(""), ex.lz77_encode("a"), ex.lz77_encode("aaaa")), ([], [], [(0, 0, "a")], [(0, 0, "a"), (1, 2, "a")]))
        self.assertEqual(ex.sizes("abc"), (3, 6, 9))
        self.assertEqual((ex.rle_encode("wwwwbbw"), ex.lz77_decode([(0, 0, "x"), (1, 3, "y")]), ex.lz77_encode("ab" * 150)[-1]), ([("w", 4), ("b", 2), ("w", 1)], "xxxxy", (2, 297, "b")))
        r = random.Random(1)
        for _ in range(300):
            s = "".join(r.choice("ab ") for _ in range(r.randint(0, 40)))
            self.assertEqual(ex.rle_decode(ex.rle_encode(s)), s)
            self.assertEqual(ex.lz77_decode(ex.lz77_encode(s)), s)


if __name__ == "__main__":
    unittest.main()
