import random
import unittest

import ch17_examples as ex


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

    def test_practice(self) -> None:
        log = []
        c = ex.huffman_codes("MISSISSIPPI", log)
        self.assertEqual(c, {"S": "0", "M": "100", "P": "101", "I": "11"})
        self.assertEqual((len(ex.encode("MISSISSIPPI", c)), ex.fixed_bits("MISSISSIPPI")), (21, 22))
        self.assertEqual(round(ex.entropy_bits("MISSISSIPPI"), 2), 20.05)
        self.assertEqual(round(ex.entropy_bits("A" * 9 + "B"), 2), 4.69)
        self.assertEqual(len(ex.encode("A" * 9 + "B", ex.huffman_codes("A" * 9 + "B"))), 10)

    def test_entropy(self) -> None:
        self.assertEqual(round(ex.entropy_bits(ex.MESSAGE), 2), 57.49)
        self.assertEqual(ex.entropy_bits(""), 0)
        self.assertEqual(ex.entropy_bits("AAAA"), 0)
        import random
        rng = random.Random(16)
        for _ in range(50):
            s = "".join(rng.choice("abcdef") for _ in range(rng.randint(2, 40)))
            bits = len(ex.encode(s, ex.huffman_codes(s)))
            if len(set(s)) > 1:
                self.assertTrue(ex.entropy_bits(s) - 1e-9 <= bits < ex.entropy_bits(s) + len(s))

if __name__ == "__main__":
    unittest.main()
