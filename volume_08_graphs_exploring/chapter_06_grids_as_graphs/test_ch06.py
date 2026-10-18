import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


def components_uf(grid):
    """Independent check with union-find."""
    rows, cols = len(grid), len(grid[0])
    parent = {}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                parent[(r, c)] = (r, c)
    for (r, c) in list(parent):
        for nr, nc in ((r + 1, c), (r, c + 1)):
            if (nr, nc) in parent:
                parent[find((r, c))] = find((nr, nc))
    roots = [find(x) for x in parent]
    sizes = {}
    for x in roots:
        sizes[x] = sizes.get(x, 0) + 1
    return len(sizes), max(sizes.values(), default=0)


class TestGrids(unittest.TestCase):
    def test_islands_random(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            cols = rng.randint(1, 8)
            g = [[rng.choice("#..") for _ in range(cols)] for _ in range(rng.randint(1, 8))]
            count, biggest = components_uf(g)
            self.assertEqual(ex.count_islands(g), count)
            self.assertEqual(sol.largest_island(g), biggest)

    def test_examples(self) -> None:
        self.assertEqual(ex.count_islands(ex.to_grid(["##..#", "#...#", "..#..", "....#"])), 4)
        self.assertEqual(["".join(r) for r in ex.flood_fill(ex.to_grid(["aab", "abb", "bbb"]), 0, 0, "z")], ["zzb", "zbb", "bbb"])
        self.assertEqual(ex.flood_fill(ex.to_grid(["aa"]), 0, 0, "a"), [["a", "a"]])
        self.assertEqual(ex.rotting_minutes(ex.to_grid(["RF.", "FF.", ".FF"])), 4)
        self.assertEqual(ex.rotting_minutes(ex.to_grid(["RF", ".F", "F."])), -1)
        self.assertEqual(ex.rotting_minutes(ex.to_grid(["..", ".."])), 0)
        maze = ex.to_grid(["S..#", ".#..", "...#", "#.G."])
        self.assertEqual(ex.shortest_walk(maze, (0, 0), (3, 2)), 5)
        self.assertEqual(ex.shortest_walk(ex.to_grid([".#."]), (0, 0), (0, 2)), -1)

    def test_solutions(self) -> None:
        self.assertEqual(sol.distance_to_nearest_exit(ex.to_grid(["E..", ".#.", "..E"])), [[0, 1, 2], [1, -1, 1], [2, 1, 0]])
        self.assertEqual(["".join(r) for r in sol.surrounded_regions(ex.to_grid(["XXXX", "XOOX", "XXOX", "XOXX"]))],
                         ["XXXX", "XXXX", "XXXX", "XOXX"])


if __name__ == "__main__":
    unittest.main()
