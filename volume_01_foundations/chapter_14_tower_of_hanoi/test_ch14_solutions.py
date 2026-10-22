import random
import unittest

import ch14_examples as ex
import ch14_solutions as sol


def all_moves_with_disks(n: int) -> list[tuple[int, str, str]]:
    """Brute force: generate every move with ex.hanoi and replay it to see which disk moves."""
    moves: list[tuple[str, str]] = []
    ex.hanoi(n, "A", "C", "B", moves)
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    out = []
    for a, b in moves:
        disk = pegs[a].pop()
        pegs[b].append(disk)
        out.append((disk, a, b))
    return out


class TestChapter14Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.move_number(1, 1, "A", "C", "B"), (1, "A", "C"))
        self.assertEqual([sol.move_number(2, m, "A", "C", "B") for m in (1, 2, 3)],
                         [(1, "A", "B"), (2, "A", "C"), (1, "B", "C")])
        for n, m in ((0, 1), (1, 0), (1, 2), (3, 8)):
            with self.assertRaises(ValueError):
                sol.move_number(n, m, "A", "C", "B")

    def test_worked_example(self) -> None:
        self.assertEqual(sol.move_number(4, 6, "A", "C", "B"), (2, "C", "B"))
        self.assertEqual(sol.move_number(4, 8, "A", "C", "B"), (4, "A", "C"))

    def test_against_brute_force(self) -> None:
        for n in range(1, 11):
            brute = all_moves_with_disks(n)
            self.assertEqual([sol.move_number(n, m, "A", "C", "B") for m in range(1, 2 ** n)], brute)
        rng = random.Random(14)
        brute = all_moves_with_disks(14)
        for _ in range(300):
            m = rng.randint(1, 2 ** 14 - 1)
            self.assertEqual(sol.move_number(14, m, "A", "C", "B"), brute[m - 1])

    def test_huge_tower(self) -> None:
        disk, a, b = sol.move_number(64, 2 ** 63, "A", "C", "B")
        self.assertEqual((disk, a, b), (64, "A", "C"))
        disk, _, _ = sol.move_number(64, 10 ** 12, "A", "C", "B")
        self.assertEqual(disk, ((10 ** 12) & -(10 ** 12)).bit_length())   # 1 + trailing zeros of m


if __name__ == "__main__":
    unittest.main()
