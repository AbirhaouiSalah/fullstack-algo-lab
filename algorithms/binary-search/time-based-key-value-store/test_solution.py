"""Tests for Time Based Key Value Store. Add concrete assertions after confirming the API.

Use pytest; avoid treating an empty suite as a passed exercise.
"""

"""Tests and benchmark for NeetCode Time Based Key-Value Store.

Design problem: solve(operations, arguments) replays a LeetCode-style call sequence,
and every class defining set/get in solution.py is also tested and benchmarked directly.
"""
import importlib.util
import inspect
import random
import statistics
import time
from pathlib import Path

import pytest

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("generated_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")
solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)


def _candidate_functions():
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if function.__module__ == solution_module.__name__
        and (name == "solve" or name.startswith("solve_"))
    ]


def _candidate_classes():
    return [
        cls
        for _, cls in inspect.getmembers(solution_module, inspect.isclass)
        if cls.__module__ == solution_module.__name__
        and callable(getattr(cls, "set", None))
        and callable(getattr(cls, "get", None))
    ]


class _Reference:
    """Dictionary of timestamp -> value per key, answers get with a max over timestamps <= t."""

    def __init__(self):
        self.data = {}

    def set(self, key, value, timestamp):
        self.data.setdefault(key, {})[timestamp] = value

    def get(self, key, timestamp):
        candidates = [ts for ts in self.data.get(key, {}) if ts <= timestamp]
        return self.data[key][max(candidates)] if candidates else ""


def test_solution_module_loads():
    assert solution_module is not None


def test_candidate_exists():
    assert (
        _candidate_functions()
    ), "Define solve(operations, arguments) or solve_*(operations, arguments)"
    assert (
        _candidate_classes()
    ), "Define at least one class with set(key, value, timestamp) and get(key, timestamp)"


def test_example_replay():
    operations = ["TimeMap", "set", "get", "get", "set", "get"]
    arguments = [
        [],
        ["alice", "happy", 1],
        ["alice", 1],
        ["alice", 2],
        ["alice", "sad", 3],
        ["alice", 3],
    ]
    expected = [None, None, "happy", "happy", None, "sad"]
    for function in _candidate_functions():
        assert (
            function(operations, arguments) == expected
        ), f"{function.__name__} failed the example"


@pytest.mark.parametrize("cls", _candidate_classes(), ids=lambda c: c.__name__)
def test_get_behaviours(cls):
    tm = cls()
    assert tm.get("missing", 5) == ""  # unknown key
    tm.set("a", "v1", 10)
    tm.set("a", "v2", 20)
    tm.set("a", "v3", 30)
    tm.set("b", "w1", 15)
    assert tm.get("a", 9) == ""  # before the first timestamp
    assert tm.get("a", 0) == ""
    assert tm.get("a", 10) == "v1"  # exact first
    assert tm.get("a", 19) == "v1"  # between
    assert tm.get("a", 20) == "v2"  # exact middle
    assert tm.get("a", 29) == "v2"
    assert tm.get("a", 30) == "v3"  # exact last
    assert tm.get("a", 10_000_000) == "v3"  # after the last
    assert tm.get("b", 14) == ""  # keys are independent
    assert tm.get("b", 15) == "w1"
    assert tm.get("b", 100) == "w1"


@pytest.mark.parametrize("cls", _candidate_classes(), ids=lambda c: c.__name__)
def test_timestamp_zero_and_single_entry(cls):
    tm = cls()
    tm.set("k", "only", 0)
    assert tm.get("k", 0) == "only"
    assert tm.get("k", 1) == "only"


def test_randomized_against_reference():
    rng = random.Random(42)
    for _ in range(100):
        keys = [f"k{i}" for i in range(rng.randrange(1, 5))]
        timestamp = 0
        operations = ["TimeMap"]
        arguments = [[]]
        reference = _Reference()
        expected = [None]
        for _ in range(rng.randrange(1, 120)):
            key = rng.choice(keys + ["unknown"])
            if rng.randrange(2):
                timestamp += rng.randrange(1, 6)  # strictly increasing, as in the constraints
                value = f"v{timestamp}"
                operations.append("set")
                arguments.append([key, value, timestamp])
                reference.set(key, value, timestamp)
                expected.append(None)
            else:
                query = rng.randrange(0, timestamp + 6)
                operations.append("get")
                arguments.append([key, query])
                expected.append(reference.get(key, query))
        for function in _candidate_functions():
            assert (
                function(operations, arguments) == expected
            ), f"{function.__name__} diverged from the reference"


def test_out_of_order_variant_handles_any_order_and_overwrites():
    rng = random.Random(7)
    cls = solution_module.TimeMapOutOfOrder
    for _ in range(100):
        tm, reference = cls(), _Reference()
        for _ in range(rng.randrange(1, 60)):
            timestamp = rng.randrange(0, 40)  # duplicates and any order allowed
            value = f"v{rng.randrange(1000)}"
            tm.set("k", value, timestamp)
            reference.set("k", value, timestamp)
        for query in range(-1, 45):
            assert tm.get("k", query) == reference.get("k", query)


def test_large_input_within_constraints():
    for cls in _candidate_classes():
        if cls.__name__ == "TimeMapLinear":
            continue  # O(n) per get, covered by the small tests
        tm = cls()
        for i in range(100_000):
            tm.set("big", f"v{i}", i * 3)
        assert tm.get("big", 0) == "v0"
        assert tm.get("big", 299_997) == "v99999"
        assert tm.get("big", 150_001) == "v50000"


def run_benchmark():
    sizes = [10, 100, 1_000, 10_000, 100_000]
    rng = random.Random(42)
    classes = _candidate_classes()
    print("\nBenchmark Time Based Key-Value Store (une cle, timestamps croissants)")
    print(f"{'Classe':>20} | {'n valeurs':>10} | {'Operation':>12} | {'Moyenne (us)':>13}")
    print("-" * 68)
    for cls in classes:
        for size in sizes:
            # Build is timed as the 'set' scenario, queries are generated outside the timed section.
            timestamps = [10 * (i + 1) for i in range(size)]
            values = [f"v{i}" for i in range(size)]
            tm = cls()
            start = time.perf_counter_ns()
            for timestamp, value in zip(timestamps, values):
                tm.set("key", value, timestamp)
            set_us = (time.perf_counter_ns() - start) / size / 1_000
            print(f'{cls.__name__:>20} | {size:>10,} | {"set":>12} | {set_us:>13.3f}')

            query_count = 1_000 if size <= 10_000 else 300
            scenarios = [
                ("get present", [rng.randrange(10, 10 * size + 50) for _ in range(query_count)]),
                ("get avant 1er", [rng.randrange(0, 10) for _ in range(query_count)]),
            ]
            for scenario, queries in scenarios:
                expected = [values[min(q // 10, size) - 1] if q >= 10 else "" for q in queries]
                if [tm.get("key", q) for q in queries] != expected:
                    print(f"{cls.__name__:>20} | {size:>10,} | {scenario:>12} | ECHEC")
                    continue
                samples = []
                for _ in range(5):
                    start = time.perf_counter_ns()
                    for q in queries:
                        tm.get("key", q)
                    samples.append((time.perf_counter_ns() - start) / len(queries) / 1_000)
                print(
                    f"{cls.__name__:>20} | {size:>10,} | {scenario:>12} | {statistics.median(samples):>13.3f}"
                )
    if not classes:
        print("Aucune classe avec set/get trouvee.")


if __name__ == "__main__":
    run_benchmark()
