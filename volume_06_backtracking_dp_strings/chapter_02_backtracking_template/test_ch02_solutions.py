import itertools
import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


def brute_round(readers, feuds):
    n = len(readers)
    out = []
    for p in itertools.permutations(readers[1:]):
        row = [readers[0], *p]
        pairs = list(zip(row, row[1:])) + ([(row[-1], row[0])] if n >= 3 else [])
        if not any(ex.clash(a, b, feuds) for a, b in pairs):
            out.append(row)
    return out


class TestChapter02Solutions(unittest.TestCase):
    def test_round_table(self) -> None:
        self.assertEqual(sol.round_seatings([], []), [[]])
        self.assertEqual(sol.round_seatings(["Ana"], []), [["Ana"]])
        self.assertEqual(sol.round_seatings(["Ana", "Ben"], [("Ana", "Ben")]), [])
        self.assertEqual(sol.round_seatings(["Ana", "Ben", "Cai"], [("Ana", "Ben")]), [])
        self.assertEqual(len(sol.round_seatings(ex.READERS, ex.FEUDS)), 16)
        r = random.Random(2)
        for _ in range(60):
            n = r.randint(1, 6)
            people = ex.READERS[:n]
            feuds = [p for p in itertools.combinations(people, 2) if r.random() < 0.3]
            self.assertEqual(sol.round_seatings(people, feuds), brute_round(people, feuds))

    def test_thinking_problems(self) -> None:
        self.assertEqual(sol.too_strict(["Ana", "Ben", "Cai"], [("Ana", "Ben")]), [])
        out, c = [], [0]
        ex.backtrack(["Ana", "Ben", "Cai"], [("Ana", "Ben")], [], out, c)
        self.assertEqual(out, [["Ana", "Cai", "Ben"], ["Ben", "Cai", "Ana"]])
        self.assertEqual(ex.first_only(ex.READERS, ex.FEUDS)[1], 10)
        self.assertEqual(ex.first_only(ex.READERS, ex.FEUDS + [("Dev", "Fay")]), (["Ana", "Cai", "Eva", "Dev", "Ben", "Fay"], 16))
        self.assertEqual(ex.work(ex.READERS, ex.FEUDS + [("Dev", "Fay")], True)[0], 379)


if __name__ == "__main__":
    unittest.main()
