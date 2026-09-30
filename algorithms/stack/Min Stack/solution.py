class MinStack:
    """Optimal solution: each entry stores (value, minimum up to this entry).

    push / pop / top / get_min are all O(1) time, O(n) extra space.
    """

    def __init__(self) -> None:
        self._values: list[tuple[int, int]] = []

    def push(self, value: int) -> None:
        current_minimum = min(value, self._values[-1][1]) if self._values else value
        self._values.append((value, current_minimum))

    def pop(self) -> None:
        if not self._values:
            raise IndexError("pop from empty MinStack")
        self._values.pop()

    def top(self) -> int:
        if not self._values:
            raise IndexError("top from empty MinStack")
        return self._values[-1][0]

    def get_min(self) -> int:
        if not self._values:
            raise IndexError("minimum from empty MinStack")
        return self._values[-1][1]


class MinStackHint1:
    """Hint 1 (brute force): scan the whole stack on every get_min.

    push / pop / top are O(1) but get_min is O(n).
    """

    def __init__(self) -> None:
        self._values: list[int] = []

    def push(self, value: int) -> None:
        self._values.append(value)

    def pop(self) -> None:
        if not self._values:
            raise IndexError("pop from empty MinStack")
        self._values.pop()

    def top(self) -> int:
        if not self._values:
            raise IndexError("top from empty MinStack")
        return self._values[-1]

    def get_min(self) -> int:
        if not self._values:
            raise IndexError("minimum from empty MinStack")
        return min(self._values)


class MinStackHint2:
    """Hint 2 (prefix approach): keep a value and its prefix minimum in each entry.

    The minimum of the stack is always the prefix minimum of its top entry,
    so get_min is O(1).
    """

    def __init__(self) -> None:
        self._entries: list[tuple[int, int]] = []

    def push(self, value: int) -> None:
        if self._entries:
            prefix_minimum = min(value, self._entries[-1][1])
        else:
            prefix_minimum = value
        self._entries.append((value, prefix_minimum))

    def pop(self) -> None:
        if not self._entries:
            raise IndexError("pop from empty MinStack")
        self._entries.pop()

    def top(self) -> int:
        if not self._entries:
            raise IndexError("top from empty MinStack")
        return self._entries[-1][0]

    def get_min(self) -> int:
        if not self._entries:
            raise IndexError("minimum from empty MinStack")
        return self._entries[-1][1]


class MinStackHint3:
    """Hint 3: main stack + extra stack holding the prefix minimum.

    Every push onto the main stack pushes min(top of min stack, value) onto the
    extra stack; every pop pops both, so the two stacks always have equal length.
    """

    def __init__(self) -> None:
        self._values: list[int] = []
        self._minimums: list[int] = []

    def push(self, value: int) -> None:
        self._values.append(value)
        if self._minimums:
            value = min(value, self._minimums[-1])
        self._minimums.append(value)

    def pop(self) -> None:
        if not self._values:
            raise IndexError("pop from empty MinStack")
        self._values.pop()
        self._minimums.pop()

    def top(self) -> int:
        if not self._values:
            raise IndexError("top from empty MinStack")
        return self._values[-1]

    def get_min(self) -> int:
        if not self._minimums:
            raise IndexError("minimum from empty MinStack")
        return self._minimums[-1]
