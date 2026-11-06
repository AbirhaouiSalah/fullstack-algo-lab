"""Tests for Search In Rotated Sorted Array. Add concrete assertions after confirming the API.

Use pytest; avoid treating an empty suite as a passed exercise.
"""

"""Tests and benchmark for NeetCode Search in Rotated Sorted Array."""
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


def _rotate(sorted_nums, k):
    """Rotate k times: the last k elements move to the front."""
    k %= len(sorted_nums)
    return sorted_nums[len(sorted_nums) - k :] + sorted_nums[: len(sorted_nums) - k]


def test_solution_module_loads():
    assert solution_module is not None


def test_candidate_exists():
    assert _candidate_functions(), "Define solve(nums, target) or solve_*(nums, target)"


CASES = [
    ([3, 4, 5, 6, 1, 2], 1, 4),
    ([3, 5, 6, 0, 1, 2], 4, -1),
    ([4, 5, 6, 7, 0, 1, 2], 0, 4),
    ([4, 5, 6, 7, 0, 1, 2], 3, -1),
    ([1], 1, 0),
    ([1], 0, -1),
    ([1, 3], 3, 1),
    ([3, 1], 1, 1),
    ([3, 1], 3, 0),
    ([3, 1], 2, -1),
    ([1, 2, 3, 4, 5], 5, 4),
    ([1, 2, 3, 4, 5], 6, -1),
    ([5, 1, 2, 3, 4], 5, 0),
    ([5, 1, 2, 3, 4], 4, 4),
    ([-3, -2, -1, 0], -3, 0),
    ([0, -3, -2, -1], -3, 1),
    ([-1000, 1000], 1000, 1),
    ([1000, -1000], -1000, 1),
]


@pytest.mark.parametrize("nums,target,expected", CASES)
def test_search_rotated_cases(nums, target, expected):
    for function in _candidate_functions():
        actual = function(nums.copy(), target)
        assert (
            actual == expected
        ), f"{function.__name__}({nums}, {target}) returned {actual}, expected {expected}"


def test_exhaustive_all_rotations_and_targets():
    """Every size 1..25, every rotation (incl. the full turn), every target from min - 1 to max + 1."""
    for size in range(1, 26):
        base = list(range(-5, size - 5))
        for k in range(size + 1):
            nums = _rotate(base, k)
            for target in range(base[0] - 1, base[-1] + 2):
                expected = nums.index(target) if target in nums else -1
                for function in _candidate_functions():
                    assert (
                        function(nums.copy(), target) == expected
                    ), f"{function.__name__}({nums}, {target}) expected {expected}"


def test_randomized_against_reference():
    rng = random.Random(42)
    for _ in range(200):
        size = rng.randrange(1, 200)
        base = sorted(rng.sample(range(-1000, 1001), size))
        nums = _rotate(base, rng.randrange(0, size + 1))
        for target in [rng.choice(nums), rng.randrange(-1000, 1001)]:
            expected = nums.index(target) if target in nums else -1
            for function in _candidate_functions():
                assert (
                    function(nums.copy(), target) == expected
                ), f"{function.__name__}({nums}, {target}) expected {expected}"


def test_input_not_mutated():
    nums = [4, 5, 6, 7, 0, 1, 2]
    snapshot = nums.copy()
    for function in _candidate_functions():
        function(nums, 0)
        assert nums == snapshot, f"{function.__name__} mutated its input"


def _arguments_for(function, nums, target):
    signature = inspect.signature(function)
    try:
        signature.bind(nums, target)
    except TypeError:
        return None
    return (nums, target)


def run_benchmark():
    sizes = [100, 1_000, 10_000, 100_000, 1_000_000]
    repetitions = 1_000
    rng = random.Random(42)
    candidates = _candidate_functions()
    print("\nBenchmark Search in Rotated Sorted Array (valeurs distinctes)")
    print(f"{'Fonction':>24} | {'n':>10} | {'Scenario':>12} | {'Moyenne (us)':>13}")
    print("-" * 70)
    for function in candidates:
        for size in sizes:
            # O(n) fixture construction is deliberately outside the timed section.
            base = list(range(0, 2 * size, 2))
            rotated = _rotate(base, rng.randrange(1, size))
            scenarios = [
                ("present", rotated, rotated[rng.randrange(size)]),
                ("absent", rotated, 2 * (size // 2) + 1),  # dans l'intervalle mais absent
                ("non tournee", base, base[rng.randrange(size)]),
            ]
            for scenario, nums, target in scenarios:
                arguments = _arguments_for(function, nums, target)
                if arguments is None:
                    print(f"{function.__name__:>24} | signature non supportee")
                    break
                expected = nums.index(target) if target in nums else -1
                actual = function(*arguments)
                if actual != expected:
                    print(
                        f"{function.__name__:>24} | {size:>10,} | {scenario:>12} | ECHEC: {actual} != {expected}"
                    )
                    continue
                samples = []
                for _ in range(5):
                    start = time.perf_counter_ns()
                    for _ in range(repetitions):
                        function(*arguments)
                    samples.append((time.perf_counter_ns() - start) / repetitions / 1_000)
                print(
                    f"{function.__name__:>24} | {size:>10,} | {scenario:>12} | {statistics.median(samples):>13.3f}"
                )
    if not candidates:
        print("Aucune fonction solve ou solve_* trouvee.")


if __name__ == "__main__":
    run_benchmark()
