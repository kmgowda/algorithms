# algorithms
Python Programs of Data Structure and Algorithms

Companion code for the book series **Algorithms Simplified**.

## Layout

```
volume_01_foundations/
  chapter_01_what_is_an_algorithm/
    ch01_examples.py    # every program shown in the chapter
    ch01_solutions.py   # solutions to the chapter's exercises
    test_ch01.py        # unittest tests (standard library only)
  ...
run_tests.py            # runs every chapter's tests
tools/check_book.py     # static checks for the book's Markdown (Mermaid syntax, required sections)
```

## Requirements

Python 3.10 or newer. No third-party packages.

## Usage

```bash
python3 run_tests.py                 # all tests
python3 run_tests.py volume_01       # one volume
python3 volume_01_foundations/chapter_09_first_real_algorithms/ch09_examples.py   # run a chapter's demos
python3 tools/check_book.py /root/projects/kmg/docs/books/algorithms/kmg-book     # check the book
```
