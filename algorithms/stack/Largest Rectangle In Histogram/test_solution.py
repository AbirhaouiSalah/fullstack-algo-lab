import importlib.util
import inspect
import itertools
import random
import time
from pathlib import Path

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_histogram_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)
largest_rectangle_area = solution_module.largest_rectangle_area


def _candidate_solutions():
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if function.__module__ == solution_module.__name__
        and (name == "solve" or name.startswith("solve_hint_"))
    ]


def test_largest_rectangle_area_finds_maximum_spanning_rectangle():
    assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
    assert solution_module.solve([2, 4]) == 4


def test_largest_rectangle_area_handles_monotonic_and_equal_heights():
    assert largest_rectangle_area([2, 3, 4, 5]) == 9
    assert largest_rectangle_area([5, 4, 3, 2]) == 9
    assert largest_rectangle_area([3, 3, 3]) == 9


def test_largest_rectangle_area_handles_empty_and_zero_heights():
    assert largest_rectangle_area([]) == 0
    assert largest_rectangle_area([0, 0]) == 0


def _brute_force_largest_rectangle(heights):
    largest_area = 0
    for left in range(len(heights)):
        minimum_height = heights[left]
        for right in range(left, len(heights)):
            minimum_height = min(minimum_height, heights[right])
            largest_area = max(largest_area, minimum_height * (right - left + 1))
    return largest_area


def test_largest_rectangle_area_exhaustive_small_inputs():
    for length in range(7):
        for heights in itertools.product(range(4), repeat=length):
            values = list(heights)
            expected = _brute_force_largest_rectangle(values)
            assert largest_rectangle_area(values) == expected
            for candidate in _candidate_solutions():
                assert candidate(values) == expected, candidate.__name__


def test_largest_rectangle_area_seeded_random_inputs_match_brute_force():
    rng = random.Random(213)
    for _ in range(300):
        heights = [rng.randint(0, 100) for _ in range(rng.randint(0, 40))]
        expected = _brute_force_largest_rectangle(heights)
        for candidate in _candidate_solutions():
            assert candidate(heights) == expected, candidate.__name__



def run_benchmark():
    print("\nBenchmark: Largest Rectangle in Histogram")
    print(f"{'Solution':>24} | {'Barres':>12} | {'Temps (ms)':>12}")
    print("-" * 54)
    for candidate in _candidate_solutions():
        for size in (1_000, 10_000, 100_000):
            heights = list(range(1, size + 1))
            started = time.perf_counter()
            area = candidate(heights)
            elapsed_ms = (time.perf_counter() - started) * 1_000
            assert area > 0
            print(f"{candidate.__name__:>24} | {size:>12,} | {elapsed_ms:>12.4f}")