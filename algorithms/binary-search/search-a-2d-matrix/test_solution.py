"""Tests and benchmark for NeetCode Search a 2D Matrix."""
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


def _copy(matrix):
    return [row.copy() for row in matrix]


def test_solution_module_loads():
    assert solution_module is not None


def test_candidate_exists():
    assert _candidate_functions(), 'Define solve(matrix, target) or solve_*(matrix, target)'


CASES = [
    ([[1, 2, 4, 8], [10, 11, 12, 13], [14, 20, 30, 40]], 10, True),
    ([[1, 2, 4, 8], [10, 11, 12, 13], [14, 20, 30, 40]], 15, False),
    ([[1]], 1, True),
    ([[1]], 2, False),
    ([[1]], 0, False),
    ([[1, 3]], 3, True),
    ([[1], [3]], 3, True),
    ([[1], [3], [5]], 4, False),
    ([[1, 2, 4, 8], [10, 11, 12, 13], [14, 20, 30, 40]], 1, True),
    ([[1, 2, 4, 8], [10, 11, 12, 13], [14, 20, 30, 40]], 40, True),
    ([[1, 2, 4, 8], [10, 11, 12, 13], [14, 20, 30, 40]], 0, False),
    ([[1, 2, 4, 8], [10, 11, 12, 13], [14, 20, 30, 40]], 41, False),
    ([[-10000, -5], [0, 10000]], -10000, True),
    ([[-10000, -5], [0, 10000]], 10000, True),
    ([[-10000, -5], [0, 10000]], -4, False),
]


@pytest.mark.parametrize('matrix,target,expected', CASES)
def test_search_matrix_cases(matrix, target, expected):
    for function in _candidate_functions():
        actual = function(_copy(matrix), target)
        assert actual is expected, f'{function.__name__}({matrix}, {target}) returned {actual}, expected {expected}'


def _random_matrix(rng, m, n):
    """Rows non decreasing (duplicates allowed), each first value > previous last value."""
    matrix = []
    current = rng.randrange(-50, 50)
    for _ in range(m):
        row = []
        for _ in range(n):
            current += rng.randrange(0, 4)
            row.append(current)
        matrix.append(row)
        current += rng.randrange(1, 4)
    return matrix


def test_randomized_against_reference():
    rng = random.Random(42)
    for _ in range(300):
        m, n = rng.randrange(1, 9), rng.randrange(1, 9)
        matrix = _random_matrix(rng, m, n)
        low, high = matrix[0][0] - 2, matrix[-1][-1] + 2
        for target in range(low, high + 1):
            expected = any(target in row for row in matrix)
            for function in _candidate_functions():
                assert function(_copy(matrix), target) is expected, (
                    f'{function.__name__}({matrix}, {target}) expected {expected}'
                )


def test_input_not_mutated():
    matrix = [[1, 3, 5], [7, 9, 11]]
    snapshot = _copy(matrix)
    for function in _candidate_functions():
        function(matrix, 9)
        assert matrix == snapshot, f'{function.__name__} mutated its input'


def _arguments_for(function, matrix, target):
    signature = inspect.signature(function)
    try:
        signature.bind(matrix, target)
    except TypeError:
        return None
    return (matrix, target)


def run_benchmark():
    sides = [10, 100, 300, 1_000]  # matrices side x side
    repetitions = 1_000
    rng = random.Random(42)
    candidates = _candidate_functions()
    print('\nBenchmark Search a 2D Matrix (lignes triees, debut > fin de la ligne precedente)')
    print(f"{'Fonction':>24} | {'m x n':>11} | {'Scenario':>9} | {'Moyenne (us)':>13}")
    print('-' * 70)
    for function in candidates:
        for side in sides:
            # O(m * n) fixture construction is deliberately outside the timed section.
            matrix = [[2 * (i * side + j) for j in range(side)] for i in range(side)]
            total = side * side
            scenarios = [
                ('present', 2 * rng.randrange(total)),
                ('absent', 2 * (total // 2) + 1),  # dans l'intervalle mais absent
            ]
            for scenario, target in scenarios:
                arguments = _arguments_for(function, matrix, target)
                if arguments is None:
                    print(f'{function.__name__:>24} | signature non supportee')
                    break
                expected = scenario == 'present'
                actual = function(*arguments)
                label = f'{side}x{side}'
                if actual is not expected:
                    print(f'{function.__name__:>24} | {label:>11} | {scenario:>9} | ECHEC: {actual} != {expected}')
                    continue
                samples = []
                for _ in range(5):
                    start = time.perf_counter_ns()
                    for _ in range(repetitions):
                        function(*arguments)
                    samples.append((time.perf_counter_ns() - start) / repetitions / 1_000)
                print(f'{function.__name__:>24} | {label:>11} | {scenario:>9} | {statistics.median(samples):>13.3f}')
    if not candidates:
        print('Aucune fonction solve ou solve_* trouvee.')


if __name__ == '__main__':
    run_benchmark()