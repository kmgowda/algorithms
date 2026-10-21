# algorithms
Python Programs of Data Structure and Algorithms

Companion code for the book series **Algorithms Simplified**.

## Layout

One folder per volume of the six-volume series, one folder per chapter inside it:

| Folder | Book |
|---|---|
| `volume_01_foundations/` | Volume 1, Foundations |
| `volume_02_hashing_trees_heaps/` | Volume 2, Data Structures |
| `volume_03_searching_sorting_graphs/` | Volume 3, Searching, Sorting, and Graph Exploration |
| `volume_04_paths_and_design/` | Volume 4, Shortest Paths and Algorithm Design |
| `volume_05_dynamic_programming_strings/` | Volume 5, Dynamic Programming and Strings |

```
volume_01_foundations/
  chapter_01_what_is_an_algorithm/
    ch01_examples.py    # every program shown in the chapter
    ch01_solutions.py   # solutions to the chapter's exercises (where the chapter has them)
    test_ch01.py        # unittest tests (standard library only)
  ...
run_tests.py            # runs every chapter's tests
```

Chapter numbers restart at 1 in every volume, matching the books. Folders for Volumes 4-6 are added as those volumes are
written.

## Requirements

Python 3.10 or newer. No third-party packages.

## Usage

```bash
python3 run_tests.py                 # all tests
python3 run_tests.py volume_02_hashing   # one volume (any part of the folder name)
python3 volume_01_foundations/chapter_09_first_real_algorithms/ch09_examples.py   # run a chapter's demos
```
