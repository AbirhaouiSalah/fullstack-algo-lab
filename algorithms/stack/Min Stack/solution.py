class MinStack:
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