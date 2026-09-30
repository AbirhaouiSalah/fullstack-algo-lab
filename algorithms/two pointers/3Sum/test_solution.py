import importlib.util
import inspect
import itertools
import random
import time
from pathlib import Path

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("two_pointers_three_sum", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)


def _candidates():
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if name == "solve" or name.startswith("solve_hint_")
    ]


def _reference(numbers: list[int]) -> list[list[int]]:
    triplets = {
        tuple(sorted((numbers[first], numbers[second], numbers[third])))
        for first, second, third in itertools.combinations(range(len(numbers)), 3)
        if numbers[first] + numbers[second] + numbers[third] == 0
    }
    return [list(triplet) for triplet in sorted(triplets)]


def _assert_candidates(numbers: list[int], expected: list[list[int]]) -> None:
    for candidate in _candidates():
        actual = candidate(numbers[:])
        if actual is not None:
            assert sorted(map(tuple, actual)) == sorted(map(tuple, expected)), candidate.__name__


def test_three_sum_examples_and_duplicate_handling():
    for numbers in (
        [-1, 0, 1, 2, -1, -4],
        [],
        [0],
        [0, 0, 0],
        [0, 0, 0, 0],
        [1, 2, -2, -1],
        [-2, 0, 1, 1, 2],
    ):
        _assert_candidates(numbers, _reference(numbers))


def test_three_sum_exhaustive_small_inputs():
    for numbers in itertools.product(range(-2, 3), repeat=5):
        values = list(numbers)
        _assert_candidates(values, _reference(values))


def test_three_sum_seeded_random_inputs():
    rng = random.Random(313)
    for _ in range(200):
        numbers = [rng.randint(-20, 20) for _ in range(rng.randint(3, 14))]
        _assert_candidates(numbers, _reference(numbers))


def run_benchmark():
    print("\nBenchmark: 3Sum")
    print(f"{'Solver':>20} | {'Numbers':>12} | {'Time (ms)':>12}")
    print("-" * 50)
    for candidate in _candidates():
        for size in (100, 500, 1_000):
            numbers = [((index * 37) % 2_001) - 1_000 for index in range(size)]
            started = time.perf_counter()
            result = candidate(numbers)
            elapsed_ms = (time.perf_counter() - started) * 1_000
            if result is None:
                print(f"{candidate.__name__:>20} | {size:>12,} | {'incomplete':>12}")
                break
            print(f"{candidate.__name__:>20} | {size:>12,} | {elapsed_ms:>12.4f}")
