"""Tests and benchmark for NeetCode Binary Search (sorted distinct integers)."""
import importlib.util
import inspect
import itertools
import random
import statistics
import time
from pathlib import Path

import pytest

solution_path = Path(__file__).with_name('solution.py')
spec = importlib.util.spec_from_file_location('generated_solution', solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f'Cannot load solution from {solution_path}')
solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)


def _candidate_functions():
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if function.__module__ == solution_module.__name__
        and (name == 'solve' or name.startswith('solve_'))
    ]


def test_solution_module_loads():
    assert solution_module is not None


def test_candidate_exists():
    assert _candidate_functions(), 'Define solve(nums, target) or solve_*(nums, target)'


CASES = [
    ([-1, 0, 3, 5, 9, 12], 9, 4),
    ([-1, 0, 3, 5, 9, 12], 2, -1),
    ([-1, 0, 2, 4, 6, 8], 4, 3),
    ([-1, 0, 2, 4, 6, 8], 3, -1),
    ([5], 5, 0),
    ([5], 3, -1),
    ([-10, -3, 0, 4, 8], -10, 0),
    ([-10, -3, 0, 4, 8], 8, 4),
    ([-10, -3, 0, 4, 8], -11, -1),
    ([-10, -3, 0, 4, 8], 9, -1),
    ([], 42, -1),
]


@pytest.mark.parametrize('nums,target,expected', CASES)
def test_binary_search_cases(nums, target, expected):
    for function in _candidate_functions():
        actual = function(nums.copy(), target)
        assert actual == expected, f'{function.__name__}({nums}, {target}) returned {actual}, expected {expected}'


def test_exhaustive_small_arrays():
    """Every sorted subset of range(-3, 7) against every target in range(-4, 8)."""
    universe = range(-3, 7)
    for size in range(0, len(universe) + 1):
        for nums in itertools.combinations(universe, size):
            nums = list(nums)
            for target in range(-4, 8):
                expected = nums.index(target) if target in nums else -1
                for function in _candidate_functions():
                    assert function(nums.copy(), target) == expected, (
                        f'{function.__name__}({nums}, {target})'
                    )


def test_randomized_against_reference():
    rng = random.Random(42)
    for _ in range(100):
        nums = sorted(rng.sample(range(-10_000, 10_001), rng.randrange(0, 150)))
        target = rng.choice(nums) if nums and rng.randrange(2) else rng.randrange(-10_000, 10_001)
        expected = nums.index(target) if target in nums else -1
        for function in _candidate_functions():
            assert function(nums.copy(), target) == expected


def test_input_not_mutated():
    nums = [-5, -1, 0, 3, 7, 11]
    snapshot = nums.copy()
    for function in _candidate_functions():
        function(nums, 3)
        assert nums == snapshot, f'{function.__name__} mutated its input'


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
    print('\nBenchmark Binary Search (entrees triees, sans doublons)')
    print(f"{'Fonction':>24} | {'n':>10} | {'Scenario':>9} | {'Moyenne (us)':>13}")
    print('-' * 70)
    for function in candidates:
        for size in sizes:
            # O(n) fixture construction is deliberately outside the timed section.
            nums = list(range(0, 2 * size, 2))
            scenarios = [('present', nums[rng.randrange(size)]), ('absent', 2 * size + 1)]
            for scenario, target in scenarios:
                arguments = _arguments_for(function, nums, target)
                if arguments is None:
                    print(f'{function.__name__:>24} | signature non supportee')
                    break
                expected = nums.index(target) if scenario == 'present' else -1
                actual = function(*arguments)
                if actual != expected:
                    print(f'{function.__name__:>24} | {size:>10,} | {scenario:>9} | ECHEC: {actual} != {expected}')
                    continue
                samples = []
                for _ in range(5):
                    start = time.perf_counter_ns()
                    for _ in range(repetitions):
                        function(*arguments)
                    samples.append((time.perf_counter_ns() - start) / repetitions / 1_000)
                print(f'{function.__name__:>24} | {size:>10,} | {scenario:>9} | {statistics.median(samples):>13.3f}')
    if not candidates:
        print('Aucune fonction solve ou solve_* trouvee.')


if __name__ == '__main__':
    run_benchmark()