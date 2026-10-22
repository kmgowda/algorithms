import random
import unittest

import ch10_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_ring_insert_moves(self) -> None:
        self.assertEqual([sol.ring_insert_moves(0, 0), sol.ring_insert_moves(1, 0), sol.ring_insert_moves(1, 1)],
                         [0, 0, 0])
        self.assertEqual([sol.ring_insert_moves(9, k) for k in range(10)], [0, 1, 2, 3, 4, 4, 3, 2, 1, 0])

    def test_gap_buffer_smallest(self) -> None:
        g = sol.GapBuffer(0)
        self.assertEqual((g.text(), len(g), g.delete()), ("", 0, None))
        g.move_to(5)
        g.insert("a")
        self.assertEqual((g.text(), g.gap_start), ("a", 1))
        g.move_to(-3)
        self.assertEqual(g.delete(), None)
        g.insert("b")
        self.assertEqual(g.text(), "ba")

    def test_gap_buffer_example(self) -> None:
        g = sol.GapBuffer(4)
        for ch in "SHELF":
            g.insert(ch)
        g.move_to(0)
        g.insert("A")
        g.insert(" ")
        self.assertEqual(g.text(), "A SHELF")

    def test_gap_buffer_against_list(self) -> None:
        rng = random.Random(10)
        for _ in range(200):
            g, model, cur = sol.GapBuffer(rng.randint(0, 3)), [], 0
            for _ in range(60):
                op = rng.random()
                if op < 0.5:
                    ch = rng.choice("abc")
                    g.insert(ch)
                    model.insert(cur, ch)
                    cur += 1
                elif op < 0.7:
                    got = g.delete()
                    self.assertEqual(got, model.pop(cur - 1) if cur else None)
                    cur = max(0, cur - 1)
                else:
                    p = rng.randint(-2, len(model) + 2)
                    g.move_to(p)
                    cur = max(0, min(p, len(model)))
                self.assertEqual((g.text(), g.gap_start, len(g)), ("".join(model), cur, len(model)))


if __name__ == "__main__":
    unittest.main()
