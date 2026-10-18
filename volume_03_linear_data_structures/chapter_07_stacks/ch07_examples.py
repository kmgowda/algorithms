"""Volume 3, Chapter 7 - Stacks: Last In, First Out.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

from typing import Any


class ArrayStack:
    """A stack on a Python list: the END of the list is the top. push/pop/peek are amortized O(1)."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def push(self, item: Any) -> None:
        self._items.append(item)

    def pop(self) -> Any:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


class _Node:
    def __init__(self, value: Any, below: "_Node | None") -> None:
        self.value = value
        self.below = below


class LinkedStack:
    """The same interface on linked nodes: the HEAD is the top. Every operation is worst-case O(1)."""

    def __init__(self) -> None:
        self._top: _Node | None = None
        self._size = 0

    def push(self, item: Any) -> None:
        self._top = _Node(item, self._top)
        self._size += 1

    def pop(self) -> Any:
        if self._top is None:
            raise IndexError("pop from empty stack")
        node = self._top
        self._top = node.below
        self._size -= 1
        return node.value

    def peek(self) -> Any:
        if self._top is None:
            raise IndexError("peek at empty stack")
        return self._top.value

    def is_empty(self) -> bool:
        return self._top is None

    def __len__(self) -> int:
        return self._size


# ------------------------------------------------------------------ applications
def is_balanced(text: str) -> bool:
    """LeetCode 20: every bracket closes the most recent unclosed bracket of the same kind."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = ArrayStack()
    for ch in text:
        if ch in "([{":
            stack.push(ch)
        elif ch in pairs:
            if stack.is_empty() or stack.pop() != pairs[ch]:
                return False
    return stack.is_empty()


class TextEditor:
    """Industry example: undo and redo with two stacks."""

    def __init__(self) -> None:
        self.text = ""
        self._undo = ArrayStack()
        self._redo = ArrayStack()

    def type(self, words: str) -> None:
        self._undo.push(self.text)
        self._redo = ArrayStack()           # a new action makes old 'redo' history meaningless
        self.text += words

    def undo(self) -> None:
        if not self._undo.is_empty():
            self._redo.push(self.text)
            self.text = self._undo.pop()

    def redo(self) -> None:
        if not self._redo.is_empty():
            self._undo.push(self.text)
            self.text = self._redo.pop()


class BrowserHistory:
    """Industry example (LeetCode 1472 idea): back and forward buttons as two stacks."""

    def __init__(self, home: str) -> None:
        self.current = home
        self._back = ArrayStack()
        self._forward = ArrayStack()

    def visit(self, url: str) -> None:
        self._back.push(self.current)
        self.current = url
        self._forward = ArrayStack()

    def back(self) -> str:
        if not self._back.is_empty():
            self._forward.push(self.current)
            self.current = self._back.pop()
        return self.current

    def forward(self) -> str:
        if not self._forward.is_empty():
            self._back.push(self.current)
            self.current = self._forward.pop()
        return self.current


def reverse_with_stack(items: list[Any]) -> list[Any]:
    """Beginner example: pile plates up, take them off - they come out reversed."""
    stack = LinkedStack()
    for item in items:
        stack.push(item)
    return [stack.pop() for _ in range(len(stack))]


if __name__ == "__main__":
    print(reverse_with_stack(["red plate", "blue plate", "green plate"]))
    for text in ("(a[b]{c})", "(]", "((", "print(prices[0])"):
        print(f"{text!r} balanced: {is_balanced(text)}")
    editor = TextEditor()
    for chunk in ("Dear zoo, ", "please ", "feed the lions."):
        editor.type(chunk)
    editor.undo()
    editor.undo()
    editor.redo()
    print("Editor:", repr(editor.text))
    browser = BrowserHistory("home")
    for page in ("animals", "lions", "lion-cubs"):
        browser.visit(page)
    print(browser.back(), browser.back(), browser.forward())
    browser.visit("tigers")
    print(browser.forward(), "(forward history cleared)")
