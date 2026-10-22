# algorithms
Python Programs of Data Structure and Algorithms

Companion code for the book series **Algorithms Simplified**.

## Layout

One folder per volume of the seven-volume series, one folder per chapter inside it:

| Folder | Book |
|---|---|
| `volume_01_foundations/` | Volume 1, Foundations |
| `volume_02_linear_structures_hashing/` | Volume 2, Linear Structures and Hashing |
| `volume_03_trees_heaps/` | Volume 3, Trees and Heaps |
| `volume_04_sorting_graphs/` | Volume 4, Sorting and Graph Exploration |
| `volume_05_paths_greedy_divide/` | Volume 5, Shortest Paths, Greedy, and Divide and Conquer |
| `volume_06_backtracking_dp_strings/` | Volume 6, Backtracking, Dynamic Programming, and Strings |
| `volume_07_math_and_advanced/` | Volume 7, Mathematics and Advanced Algorithms |

```
volume_01_foundations/
  chapter_01_what_is_an_algorithm/
    ch01_examples.py    # every program shown in the chapter
    ch01_solutions.py   # solutions to the chapter's exercises (where the chapter has them)
    test_ch01.py        # unittest tests (standard library only)
  ...
run_tests.py            # runs every chapter's tests
```

Chapter numbers restart at 1 in every volume, matching the books.

## Requirements

Python 3.10 or newer. No third-party packages.

## Usage

```bash
python3 run_tests.py                 # all tests
python3 run_tests.py volume_02      # one volume (any part of the folder name)
python3 volume_01_foundations/chapter_11_binary_search/ch11_examples.py   # run a chapter's demos
```
