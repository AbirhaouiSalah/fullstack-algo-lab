"""Tests for Koko Eating Bananas. Add concrete assertions after confirming the API.

Use pytest; avoid treating an empty suite as a passed exercise.
"""
"""Tests and benchmark for NeetCode Koko Eating Bananas."""
import importlib.util
import inspect
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


def _hours(piles, k):
    return sum(-(-p // k) for p in piles)


def _linear_reference(piles, h):
    """Brute force O(n * max): fine for small values only."""
    for k in range(1, max(piles) + 1):
        if _hours(piles, k) <= h:
            return k
    raise AssertionError('unreachable: k = max(piles) always works when h >= len(piles)')


def _binary_reference(piles, h):
    """Independent binary search, used to check big benchmark inputs."""
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if _hours(piles, mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo


def test_solution_module_loads():
    assert solution_module is not None


def test_candidate_exists():
    assert _candidate_functions(), 'Define solve(piles, h) or solve_*(piles, h)'


CASES = [
    ([1, 4, 3, 2], 9, 2),
    ([25, 10, 23, 4], 4, 25),
    ([5], 5, 1),
    ([5], 1, 5),
    ([5], 2, 3),
    ([1, 1, 1, 1], 4, 1),
    ([1, 1, 1, 1], 100, 1),
    ([30, 11, 23, 4, 20], 5, 30),
    ([30, 11, 23, 4, 20], 6, 23),
    ([3, 6, 7, 11], 8, 4),
    ([312884470], 312884469, 2),
    ([805306368, 805306368, 805306368], 1_000_000_000, 3),
    ([1_000_000_000], 1_000_000_000, 1),
    ([1_000_000_000, 1_000_000_000], 2, 1_000_000_000),
]


@pytest.mark.parametrize('piles,h,expected', CASES)
def test_koko_cases(piles, h, expected):
    for function in _candidate_functions():
        actual = function(piles.copy(), h)
        assert actual == expected, f'{function.__name__}({piles}, {h}) returned {actual}, expected {expected}'


def test_exhaustive_small():
    """Every multiset of up to 3 piles in 1..8, every h from len(piles) to sum + 1."""
    for a in range(1, 9):
        for b in range(a, 9):
            for c in range(b, 9):
                for piles in ([a], [a, b], [a, b, c]):
                    for h in range(len(piles), sum(piles) + 2):
                        expected = _linear_reference(piles, h)
                        for function in _candidate_functions():
                            assert function(piles.copy(), h) == expected, (
                                f'{function.__name__}({piles}, {h}) expected {expected}'
                            )


def test_randomized_against_reference():
    rng = random.Random(42)
    for _ in range(300):
        n = rng.randrange(1, 8)
        piles = [rng.randrange(1, 60) for _ in range(n)]
        h = rng.randrange(n, sum(piles) + 3)
        expected = _linear_reference(piles, h)
        for function in _candidate_functions():
            assert function(piles.copy(), h) == expected, f'{function.__name__}({piles}, {h}) expected {expected}'


def test_randomized_large_values():
    rng = random.Random(7)
    for _ in range(100):
        n = rng.randrange(1, 50)
        piles = [rng.randrange(1, 1_000_000_001) for _ in range(n)]
        h = rng.randrange(n, min(1_000_000_000, 5 * n) + 1)
        expected = _binary_reference(piles, h)
        for function in _candidate_functions():
            assert function(piles.copy(), h) == expected, f'{function.__name__} failed on large values'


def test_result_is_minimal_and_feasible():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randrange(1, 30)
        piles = [rng.randrange(1, 1_000_000) for _ in range(n)]
        h = rng.randrange(n, 4 * n + 1)
        for function in _candidate_functions():
            k = function(piles.copy(), h)
            assert _hours(piles, k) <= h
            assert k == 1 or _hours(piles, k - 1) > h


def test_input_not_mutated():
    piles = [30, 11, 23, 4, 20]
    snapshot = piles.copy()
    for function in _candidate_functions():
        function(piles, 6)
        assert piles == snapshot, f'{function.__name__} mutated its input'


def _arguments_for(function, piles, h):
    signature = inspect.signature(function)
    try:
        signature.bind(piles, h)
    except TypeError:
        return None
    return (piles, h)


def run_benchmark():
    sizes = [10, 100, 1_000, 10_000]
    rng = random.Random(42)
    candidates = _candidate_functions()
    print('\nBenchmark Koko Eating Bananas (piles aleatoires dans [1, 10^9])')
    print(f"{'Fonction':>24} | {'n piles':>8} | {'Scenario':>9} | {'Moyenne (us)':>13}")
    print('-' * 68)
    for function in candidates:
        for size in sizes:
            # Fixture construction and reference answer are deliberately outside the timed section.
            piles = [rng.randrange(1, 1_000_000_001) for _ in range(size)]
            repetitions = max(5, 100_000 // size)
            scenarios = [('h=n', size), ('h=2n', 2 * size), ('h=10n', 10 * size)]
            for scenario, h in scenarios:
                arguments = _arguments_for(function, piles, h)
                if arguments is None:
                    print(f'{function.__name__:>24} | signature non supportee')
                    break
                expected = _binary_reference(piles, h)
                actual = function(*arguments)
                if actual != expected:
                    print(f'{function.__name__:>24} | {size:>8,} | {scenario:>9} | ECHEC: {actual} != {expected}')
                    continue
                samples = []
                for _ in range(5):
                    start = time.perf_counter_ns()
                    for _ in range(repetitions):
                        function(*arguments)
                    samples.append((time.perf_counter_ns() - start) / repetitions / 1_000)
                print(f'{function.__name__:>24} | {size:>8,} | {scenario:>9} | {statistics.median(samples):>13.3f}')
    if not candidates:
        print('Aucune fonction solve ou solve_* trouvee.')


if __name__ == '__main__':
    run_benchmark()