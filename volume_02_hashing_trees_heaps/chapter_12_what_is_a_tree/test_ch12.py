import unittest

import ch12_examples as ex


class TestChapter41(unittest.TestCase):
    def test_tree(self) -> None:
        self.assertEqual(ex.path_from_root(ex.SECTIONS, "Geometry"), ["Library", "Science", "Maths", "Geometry"])
        self.assertEqual(ex.height(ex.SECTIONS, "Library"), 3)
        self.assertEqual(ex.leaves(ex.SECTIONS, "Library"),
                         ["Mystery", "Fantasy", "Physics", "Biology", "Algebra", "Geometry", "Ancient"])
        small = {"A": ["B", "C"], "B": ["D", "E", "F"], "C": ["G"], "E": ["H"]}
        self.assertEqual(ex.height(small, "A"), 3)
        self.assertEqual(sorted(ex.leaves(small, "A")), ["D", "F", "G", "H"])
        self.assertEqual(ex.max_nodes(4), 31)
        nodes = 1 + sum(len(v) for v in ex.SECTIONS.values())
        self.assertEqual(len(ex.parents(ex.SECTIONS)), nodes - 1)


if __name__ == "__main__":
    unittest.main()
