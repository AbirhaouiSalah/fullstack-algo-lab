import importlib.util
import inspect
import random
import time
from pathlib import Path

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("two_pointers_two_sum_ii", solution_path)
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


def _reference(numbers: list[int], target: int) -> list[int]:
    for left in range(len(numbers)):
        for right in range(left + 1, len(numbers)):
            if numbers[left] + numbers[right] == target:
                return [left + 1, right + 1]
    raise ValueError("Input must contain a valid pair")


def _assert_candidates(numbers: list[int], target: int, expected: list[int]) -> None:
    for candidate in _candidates():
        actual = candidate(numbers, target)
        if actual is not None:
            assert actual == expected, f"{candidate.__name__}({numbers!r}, {target})"


def test_two_sum_ii_examples_and_edge_cases():
    examples = [
        ([-5, -2, 0, 3, 8], 1),
        ([2, 7, 11, 15], 9),
        ([2, 3, 4], 6),
        ([-1, 0], -1),
        ([1, 1], 2),
    ]
    for numbers, target in examples:
        _assert_candidates(numbers, target, _reference(numbers, target))


def test_two_sum_ii_seeded_random_inputs():
    rng = random.Random(211)
    for _ in range(300):
        numbers = sorted(rng.randint(-100, 100) for _ in range(rng.randint(2, 30)))
        left, right = sorted(rng.sample(range(len(numbers)), 2))
        target = numbers[left] + numbers[right]
        _assert_candidates(numbers, target, _reference(numbers, target))


def run_benchmark():
    print("\nBenchmark: Two Sum II")
    print(f"{'Solver':>20} | {'Numbers':>12} | {'Time (ms)':>12}")
    print("-" * 50)
    for candidate in _candidates():
        for size in (1_000, 10_000, 100_000):
            numbers = list(range(size))
            target = numbers[-2] + numbers[-1]
            started = time.perf_counter()
            result = candidate(numbers, target)
            elapsed_ms = (time.perf_counter() - started) * 1_000
            if result is None:
                print(f"{candidate.__name__:>20} | {size:>12,} | {'incomplete':>12}")
                break
            assert result == [size - 1, size]
            print(f"{candidate.__name__:>20} | {size:>12,} | {elapsed_ms:>12.4f}")
