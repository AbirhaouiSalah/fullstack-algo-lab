import importlib.util
import inspect
import itertools
import random
import time
from pathlib import Path

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("two_pointers_container_water", solution_path)
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


def _reference(heights: list[int]) -> int:
    return max(
        (
            min(heights[left], heights[right]) * (right - left)
            for left in range(len(heights))
            for right in range(left + 1, len(heights))
        ),
        default=0,
    )


def _assert_candidates(heights: list[int], expected: int) -> None:
    for candidate in _candidates():
        actual = candidate(heights[:])
        if actual is not None:
            assert actual == expected, f"{candidate.__name__}({heights!r})"


def test_container_water_examples_and_edges():
    for heights in ([1, 8, 6, 2, 5, 4, 8, 3, 7], [1, 1], [4, 3, 2, 1, 4], [1, 2, 1], []):
        _assert_candidates(list(heights), _reference(list(heights)))


def test_container_water_exhaustive_small_inputs():
    for heights in itertools.product(range(4), repeat=5):
        values = list(heights)
        _assert_candidates(values, _reference(values))


def test_container_water_seeded_random_inputs():
    rng = random.Random(419)
    for _ in range(250):
        heights = [rng.randint(0, 100) for _ in range(rng.randint(2, 30))]
        _assert_candidates(heights, _reference(heights))


def run_benchmark():
    print("\nBenchmark: Container With Most Water")
    print(f"{'Solver':>20} | {'Heights':>12} | {'Time (ms)':>12}")
    print("-" * 50)
    for candidate in _candidates():
        for size in (1_000, 10_000, 100_000):
            heights = [(index * 53) % 10_001 for index in range(size)]
            started = time.perf_counter()
            result = candidate(heights)
            elapsed_ms = (time.perf_counter() - started) * 1_000
            if result is None:
                print(f"{candidate.__name__:>20} | {size:>12,} | {'incomplete':>12}")
                break
            print(f"{candidate.__name__:>20} | {size:>12,} | {elapsed_ms:>12.4f}")
