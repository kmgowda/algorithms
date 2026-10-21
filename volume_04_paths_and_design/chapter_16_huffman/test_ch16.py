import random
import unittest

import ch16_examples as ex


class TestChapter16(unittest.TestCase):
    def test_message(self) -> None:
        log = []
        codes = ex.huffman_codes(ex.MESSAGE, log)
        bits = ex.encode(ex.MESSAGE, codes)
        self.assertEqual((len(bits), ex.fixed_bits(ex.MESSAGE), ex.decode(bits, codes)), (58, 68, ex.MESSAGE))
        self.assertEqual((codes["A"], codes[" "]), ("000", "1111"))
        self.assertEqual((log[0], log[-1][0] + log[-1][2]), ((1, "E", 1, "I"), 17))
        for a in codes.values():                      # no code is the start of another
            self.assertFalse(any(b != a and b.startswith(a) for b in codes.values()))

    def test_every_case(self) -> None:
        self.assertEqual((ex.huffman_codes(""), ex.encode("", {})), ({}, ""))
        self.assertEqual(ex.encode("AAAA", ex.huffman_codes("AAAA")), "0000")
        c = ex.huffman_codes("ABCDEFGH")
        self.assertEqual((len(ex.encode("ABCDEFGH", c)), ex.fixed_bits("ABCDEFGH")), (24, 24))
        t = "A" * 50 + "B" * 20 + "C" * 20 + "D" * 10
        c = ex.huffman_codes(t)
        self.assertEqual((c["A"], len(ex.encode(t, c)), ex.fixed_bits(t)), ("0", 180, 200))
        rng = random.Random(1)
        for _ in range(50):
            s = "".join(rng.choice("abcde") for _ in range(rng.randint(1, 30)))
            self.assertEqual(ex.decode(ex.encode(s, ex.huffman_codes(s)), ex.huffman_codes(s)), s)


if __name__ == "__main__":
    unittest.main()
