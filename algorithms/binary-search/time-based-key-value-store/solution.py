"""Time Based Key Value Store — implement after solving the problem.

Define the signature from the official statement before writing the algorithm.
"""
"""Time Based Key-Value Store: set in O(1), get in O(log n) with a handwritten binary search.

The bisect-based class is only a stdlib baseline for the benchmark and the linear class is the
brute force that shows why binary search is needed.
"""
from bisect import bisect_left, bisect_right


class TimeMap:
    """1. Par cle : deux listes paralleles (timestamps, valeurs) + binary search a la main."""

    def __init__(self):
        self.store: dict[str, tuple[list[int], list[str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = ([], [])
        timestamps, values = self.store[key]
        timestamps.append(timestamp)  # timestamps strictement croissants : append garde la liste triee
        values.append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        timestamps, values = self.store[key]

        # On cherche le plus grand index dont le timestamp est <= timestamp demande.
        l, r = 0, len(timestamps) - 1
        res = ""
        while l <= r:
            mid = l + (r - l) // 2
            if timestamps[mid] <= timestamp:
                res = values[mid]  # candidat valide, on cherche un timestamp plus recent a droite
                l = mid + 1
            else:
                r = mid - 1
        return res


class TimeMapPairs:
    """2. Par cle : une liste de couples (timestamp, valeur), binary search sur pair[0]."""

    def __init__(self):
        self.store: dict[str, list[tuple[int, str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        pairs = self.store.get(key)
        if not pairs:
            return ""

        l, r = 0, len(pairs) - 1
        res = ""
        while l <= r:
            mid = l + (r - l) // 2
            if pairs[mid][0] <= timestamp:
                res = pairs[mid][1]
                l = mid + 1
            else:
                r = mid - 1
        return res


class TimeMapBisect:
    """3. Baseline stdlib : bisect_right (ecrit en C) sur la liste des timestamps."""

    def __init__(self):
        self.store: dict[str, tuple[list[int], list[str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        timestamps, values = self.store.setdefault(key, ([], []))
        timestamps.append(timestamp)
        values.append(value)

    def get(self, key: str, timestamp: int) -> str:
        entry = self.store.get(key)
        if entry is None:
            return ""
        timestamps, values = entry
        i = bisect_right(timestamps, timestamp)
        return values[i - 1] if i else ""


class TimeMapLinear:
    """4. Force brute : parcours depuis la fin, O(n) par get."""

    def __init__(self):
        self.store: dict[str, tuple[list[int], list[str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        timestamps, values = self.store.setdefault(key, ([], []))
        timestamps.append(timestamp)
        values.append(value)

    def get(self, key: str, timestamp: int) -> str:
        entry = self.store.get(key)
        if entry is None:
            return ""
        timestamps, values = entry
        for i in range(len(timestamps) - 1, -1, -1):
            if timestamps[i] <= timestamp:
                return values[i]
        return ""


class TimeMapOutOfOrder:
    """5. Variante generale : accepte des set dans n'importe quel ordre (insertion triee, set en O(n))."""

    def __init__(self):
        self.store: dict[str, tuple[list[int], list[str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        timestamps, values = self.store.setdefault(key, ([], []))
        i = bisect_left(timestamps, timestamp)
        if i < len(timestamps) and timestamps[i] == timestamp:
            values[i] = value  # meme timestamp : on ecrase
        else:
            timestamps.insert(i, timestamp)
            values.insert(i, value)

    def get(self, key: str, timestamp: int) -> str:
        entry = self.store.get(key)
        if entry is None:
            return ""
        timestamps, values = entry

        l, r = 0, len(timestamps) - 1
        res = ""
        while l <= r:
            mid = l + (r - l) // 2
            if timestamps[mid] <= timestamp:
                res = values[mid]
                l = mid + 1
            else:
                r = mid - 1
        return res


def _replay(factory, operations: list[str], arguments: list[list]) -> list:
    """Replay a LeetCode-style call sequence: ["TimeMap", "set", "get", ...] with their arguments."""
    obj = None
    outputs: list = []
    for operation, args in zip(operations, arguments):
        if operation == 'TimeMap':
            obj = factory()
            outputs.append(None)
        elif operation == 'set':
            obj.set(*args)
            outputs.append(None)
        elif operation == 'get':
            outputs.append(obj.get(*args))
        else:
            raise ValueError(f'Unknown operation: {operation}')
    return outputs


def solve(operations: list[str], arguments: list[list]) -> list:
    return _replay(TimeMap, operations, arguments)


def solve_pairs(operations: list[str], arguments: list[list]) -> list:
    return _replay(TimeMapPairs, operations, arguments)


def solve_bisect(operations: list[str], arguments: list[list]) -> list:
    return _replay(TimeMapBisect, operations, arguments)


def solve_linear(operations: list[str], arguments: list[list]) -> list:
    return _replay(TimeMapLinear, operations, arguments)


def solve_out_of_order(operations: list[str], arguments: list[list]) -> list:
    return _replay(TimeMapOutOfOrder, operations, arguments)