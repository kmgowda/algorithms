import random
import unittest
from collections import Counter

import ch17_examples as ex
import ch17_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_kraft_and_two_queues(self) -> None:
        r = random.Random(17)
        for _ in range(200):
            text = "".join(r.choice("ABCDEFG") for _ in range(r.randint(2, 60)))
            codes = ex.huffman_codes(text)
            if len(codes) > 1:
                self.assertEqual(sol.kraft_sum(codes), 1)
            self.assertEqual(sol.two_queue_total_bits(sorted(Counter(text).values())), len(ex.encode(text, codes)))
        self.assertEqual(sol.two_queue_total_bits([]), 0)

    def test_message(self) -> None:
        codes = ex.huffman_codes(ex.MESSAGE)
        self.assertEqual(sol.two_queue_total_bits(sorted(Counter(ex.MESSAGE).values())), len(ex.encode(ex.MESSAGE, codes)))

    def test_bad_code(self) -> None:
        self.assertEqual(sorted(sol.all_parses("01", sol.BAD_CODE)), ["AC", "B"])
        codes = ex.huffman_codes(ex.MESSAGE)
        self.assertEqual(sol.all_parses(ex.encode("BOOK", codes), codes), ["BOOK"])


if __name__ == "__main__":
    unittest.main()
