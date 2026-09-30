import importlib.util
import inspect
import itertools
import random
import time
from pathlib import Path

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("two_pointers_trapping_rain_water", solution_path)
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
    water = 0
    for index, height in enumerate(heights):
        left_maximum = max(heights[: index + 1], default=0)
        right_maximum = max(heights[index:], default=0)
        water += max(0, min(left_maximum, right_maximum) - height)
    return water


def _assert_candidates(heights: list[int], expected: int) -> None:
    for candidate in _candidates():
        actual = candidate(heights[:])
        if actual is not None:
            assert actual == expected, f"{candidate.__name__}({heights!r})"


def test_trapping_rain_water_examples_and_edges():
    examples = ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], [4, 2, 0, 3, 2, 5], [], [0], [3, 3, 3])
    for heights in examples:
        _assert_candidates(list(heights), _reference(list(heights)))


def test_trapping_rain_water_exhaustive_small_inputs():
    for heights in itertools.product(range(4), repeat=6):
        values = list(heights)
        _assert_candidates(values, _reference(values))


def test_trapping_rain_water_seeded_random_inputs():
    rng = random.Random(523)
    for _ in range(250):
        heights = [rng.randint(0, 100) for _ in range(rng.randint(0, 40))]
        _assert_candidates(heights, _reference(heights))


def run_benchmark():
    print("\nBenchmark: Trapping Rain Water")
    print(f"{'Solver':>20} | {'Heights':>12} | {'Time (ms)':>12}")
    print("-" * 50)
    for candidate in _candidates():
        for size in (1_000, 10_000, 100_000):
            heights = [(index * 67) % 10_001 for index in range(size)]
            started = time.perf_counter()
            result = candidate(heights)
            elapsed_ms = (time.perf_counter() - started) * 1_000
            if result is None:
                print(f"{candidate.__name__:>20} | {size:>12,} | {'incomplete':>12}")
                break
            print(f"{candidate.__name__:>20} | {size:>12,} | {elapsed_ms:>12.4f}")
