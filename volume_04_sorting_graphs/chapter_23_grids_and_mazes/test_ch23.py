import unittest

import ch23_examples as ex


class TestChapter26(unittest.TestCase):
    def test_basement(self) -> None:
        s, e = ex.find(ex.BASEMENT, "S"), ex.find(ex.BASEMENT, "E")
        path, dist = ex.bfs_grid(ex.BASEMENT, s, e)
        self.assertEqual(len(path) - 1, 15)
        self.assertEqual(len(ex.flood_fill(ex.BASEMENT, s)), 27)
        self.assertEqual(list(ex.neighbours(ex.BASEMENT, 0, 0)), [(0, 1), (1, 0)])

    def test_every_case(self) -> None:
        self.assertEqual(ex.bfs_grid(ex.BASEMENT, (0, 0), (0, 0))[0], [(0, 0)])
        walled = ["S.#.", "..#E", "..#."]
        self.assertIsNone(ex.bfs_grid(walled, (0, 0), (1, 3))[0])
        self.assertEqual(len(ex.flood_fill(walled, (0, 0))), 6)
        self.assertEqual(len(ex.bfs_grid(["...."] * 3, (0, 0), (2, 3))[0]) - 1, 5)
        self.assertIsNone(ex.bfs_grid(["S#", "#E"], (0, 0), (1, 1))[0])
        self.assertEqual(ex.bfs_grid(["S"], (0, 0), (0, 0))[0], [(0, 0)])

    def test_maze_is_perfect(self) -> None:
        for seed in range(5):
            m = ex.generate_maze(4, 6, seed)
            opened = sum(r.count(".") for r in m)
            self.assertEqual(opened - 24, 23)               # 24 rooms + 23 knocked-down walls: a tree
            self.assertEqual(len(ex.flood_fill(m, (1, 1))), opened)
        m = ex.generate_maze(4, 6)
        self.assertEqual(len(ex.bfs_grid(m, (1, 1), (7, 11))[0]) - 1, 20)

    def test_state_graph(self) -> None:
        jam = {"100", "010", "001"}
        path = ex.bfs_states("000", "202", ex.lock_moves(jam))
        self.assertEqual(path, ["000", "900", "901", "902", "002", "102", "202"])
        self.assertEqual(len(ex.bfs_states("000", "202", ex.lock_moves(set()))) - 1, 4)
        self.assertEqual(ex.bfs_states("000", "000", ex.lock_moves(jam)), ["000"])
        boxed = {"100", "900", "010", "090", "001", "009"}
        self.assertIsNone(ex.bfs_states("000", "202", ex.lock_moves(boxed)))
        self.assertEqual(ex.count_states("000", ex.lock_moves(boxed)), 1)
        self.assertEqual(ex.count_states("000", ex.lock_moves(jam)), 997)
        self.assertEqual(sorted(ex.lock_moves(jam)("000")), ["009", "090", "900"])
        self.assertEqual(ex.bfs_states("0", "5", ex.lock_moves(set())), ["0", "1", "2", "3", "4", "5"])
        self.assertEqual(len(ex.bfs_states("000", "909", ex.lock_moves(set()))) - 1, 2)
        far = max(len(ex.bfs_states("000", f"{n:03d}", ex.lock_moves(jam))) - 1 for n in range(1000)
                  if f"{n:03d}" not in jam)
        self.assertEqual(far, 15)


if __name__ == "__main__":
    unittest.main()
