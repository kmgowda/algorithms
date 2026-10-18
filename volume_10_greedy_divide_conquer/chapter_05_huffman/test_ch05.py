import random
import unittest
from collections import Counter

import ch05_examples as ex
import ch05_solutions as sol


class TestHuffman(unittest.TestCase):
    def test_round_trip_and_optimal(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            text = "".join(rng.choice("abcdef"[:rng.randint(1, 6)]) for _ in range(rng.randint(1, 40)))
            freq = Counter(text)
            codes = ex.huffman_codes(freq)
            self.assertTrue(ex.is_prefix_free(codes))
            self.assertEqual(ex.decode(ex.encode(text, codes), codes), text)
            total = sol.weighted_length(freq, codes)
            if len(freq) > 1:
                self.assertEqual(total, sol.huffman_cost_only(list(freq.values())))
                self.assertEqual(total, sol.best_prefix_code_brute(dict(freq)))
            self.assertLessEqual(len(ex.encode(text, codes)), ex.fixed_length_bits(text))

    def test_canonical(self) -> None:
        f = {"a": 5, "b": 2, "r": 2, "c": 1, "d": 1}
        canon = sol.canonical_codes(f)
        self.assertTrue(ex.is_prefix_free(canon))
        self.assertEqual(sorted(len(c) for c in canon.values()), sorted(len(c) for c in ex.huffman_codes(f).values()))
        self.assertEqual(ex.huffman_codes({"x": 7}), {"x": "0"})

    def test_compression(self) -> None:
        h, raw = ex.compressed_bits("the lion and the tiger and the zebra ran to the river " * 20)
        self.assertLess(h, raw * 0.6)


if __name__ == "__main__":
    unittest.main()
