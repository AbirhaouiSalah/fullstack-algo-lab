"""Tests for Median of Two Sorted Arrays. Add concrete assertions after confirming the API.

Use pytest; avoid treating an empty suite as a passed exercise.
"""

"""Tests and benchmark for NeetCode Median of Two Sorted Arrays."""
import importlib.util
import inspect
import itertools
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


def _reference(nums1, nums2):
    merged = sorted(nums1 + nums2)
    mid = len(merged) // 2
    return float(merged[mid]) if len(merged) % 2 else (merged[mid - 1] + merged[mid]) / 2


def test_solution_module_loads():
    assert solution_module is not None


def test_candidate_exists():
    assert _candidate_functions(), "Define solve(nums1, nums2) or solve_*(nums1, nums2)"


CASES = [
    ([1, 2], [3], 2.0),
    ([1, 3], [2, 4], 2.5),
    ([], [1], 1.0),
    ([1], [], 1.0),
    ([], [2, 3], 2.5),
    ([2, 3], [], 2.5),
    ([1], [2], 1.5),
    ([2], [1], 1.5),
    ([1, 1], [1, 1], 1.0),
    ([1, 2, 3], [4, 5, 6], 3.5),
    ([4, 5, 6], [1, 2, 3], 3.5),
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8], 4.0),
    ([-5, -3, -1], [-4, -2, 0], -2.5),
    ([-1_000_000], [1_000_000], 0.0),
    ([0, 0], [0, 0], 0.0),
    ([1, 3], [2], 2.0),
    ([1, 2], [-1, 3], 1.5),
    ([100_000], [100_001, 100_002, 100_003], 100_001.5),
]


@pytest.mark.parametrize("nums1,nums2,expected", CASES)
def test_median_cases(nums1, nums2, expected):
    for function in _candidate_functions():
        actual = function(nums1.copy(), nums2.copy())
        assert (
            actual == expected
        ), f"{function.__name__}({nums1}, {nums2}) returned {actual}, expected {expected}"


def test_returns_float():
    for function in _candidate_functions():
        assert isinstance(
            function([1, 2, 3], [4, 5, 6, 7]), float
        ), f"{function.__name__} must return a float"
        assert isinstance(function([2], []), float)


def test_exhaustive_small_arrays():
    """Every pair of sorted arrays with up to 4 values from 0..4 (duplicates included)."""
    arrays = [
        list(c)
        for size in range(5)
        for c in itertools.combinations_with_replacement(range(5), size)
    ]
    for nums1 in arrays:
        for nums2 in arrays:
            if not nums1 and not nums2:
                continue
            expected = _reference(nums1, nums2)
            for function in _candidate_functions():
                assert (
                    function(nums1.copy(), nums2.copy()) == expected
                ), f"{function.__name__}({nums1}, {nums2}) expected {expected}"


def test_randomized_against_reference():
    rng = random.Random(42)
    for _ in range(300):
        m, n = rng.randrange(0, 60), rng.randrange(0, 60)
        if m + n == 0:
            continue
        nums1 = sorted(rng.randrange(-1_000_000, 1_000_001) for _ in range(m))
        nums2 = sorted(rng.randrange(-1_000_000, 1_000_001) for _ in range(n))
        expected = _reference(nums1, nums2)
        for function in _candidate_functions():
            assert (
                function(nums1.copy(), nums2.copy()) == expected
            ), f"{function.__name__}({nums1}, {nums2}) expected {expected}"


def test_max_size_constraints():
    rng = random.Random(1)
    nums1 = sorted(rng.randrange(-1_000_000, 1_000_001) for _ in range(1000))
    nums2 = sorted(rng.randrange(-1_000_000, 1_000_001) for _ in range(1000))
    expected = _reference(nums1, nums2)
    for function in _candidate_functions():
        assert function(nums1.copy(), nums2.copy()) == expected


def test_input_not_mutated():
    nums1, nums2 = [1, 3, 8], [2, 4]
    snapshot1, snapshot2 = nums1.copy(), nums2.copy()
    for function in _candidate_functions():
        function(nums1, nums2)
        assert nums1 == snapshot1 and nums2 == snapshot2, f"{function.__name__} mutated its input"


def _arguments_for(function, nums1, nums2):
    signature = inspect.signature(function)
    try:
        signature.bind(nums1, nums2)
    except TypeError:
        return None
    return (nums1, nums2)


def run_benchmark():
    sizes = [10, 100, 1_000, 10_000, 100_000]
    rng = random.Random(42)
    candidates = _candidate_functions()
    print("\nBenchmark Median of Two Sorted Arrays (m = n sauf scenario inegal)")
    print(f"{'Fonction':>24} | {'n':>8} | {'Scenario':>12} | {'Moyenne (us)':>13}")
    print("-" * 68)
    for function in candidates:
        for size in sizes:
            # O(n) fixture construction and reference answer are deliberately outside the timed section.
            scenarios = [
                ("entrelaces", list(range(0, 2 * size, 2)), list(range(1, 2 * size, 2))),
                ("disjoints", list(range(size)), list(range(size, 2 * size))),
                (
                    "inegaux",
                    sorted(rng.randrange(-(10**6), 10**6 + 1) for _ in range(10)),
                    sorted(rng.randrange(-(10**6), 10**6 + 1) for _ in range(size)),
                ),
            ]
            repetitions = max(5, 20_000 // size)
            for scenario, nums1, nums2 in scenarios:
                arguments = _arguments_for(function, nums1, nums2)
                if arguments is None:
                    print(f"{function.__name__:>24} | signature non supportee")
                    break
                expected = _reference(nums1, nums2)
                actual = function(*arguments)
                if actual != expected:
                    print(
                        f"{function.__name__:>24} | {size:>8,} | {scenario:>12} | ECHEC: {actual} != {expected}"
                    )
                    continue
                samples = []
                for _ in range(5):
                    start = time.perf_counter_ns()
                    for _ in range(repetitions):
                        function(*arguments)
                    samples.append((time.perf_counter_ns() - start) / repetitions / 1_000)
                print(
                    f"{function.__name__:>24} | {size:>8,} | {scenario:>12} | {statistics.median(samples):>13.3f}"
                )
    if not candidates:
        print("Aucune fonction solve ou solve_* trouvee.")


if __name__ == "__main__":
    run_benchmark()
