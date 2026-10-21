import unittest

import ch26_examples as ex


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


if __name__ == "__main__":
    unittest.main()
