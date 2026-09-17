import importlib.util
import inspect
import random
import time
from pathlib import Path

import pytest


solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("longest_consecutive_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        # --- Provided examples ---
        ([2, 20, 4, 10, 3, 4, 5], 4),
        ([0, 3, 2, 5, 4, 6, 1, 1], 7),

        # --- Empty / single element ---
        ([], 0),
        ([5], 1),
        ([0], 1),
        ([-1], 1),

        # --- Already sorted consecutive ---
        ([1, 2, 3, 4, 5], 5),
        ([0, 1, 2], 3),
        ([-3, -2, -1, 0, 1], 5),

        # --- Fully consecutive but shuffled ---
        ([5, 3, 1, 4, 2], 5),
        ([10, 7, 9, 8, 6], 5),

        # --- All duplicates ---
        ([7, 7, 7, 7], 1),
        ([0, 0, 0], 1),
        ([-5, -5, -5, -5, -5], 1),

        # --- Duplicates inside a run ---
        ([1, 2, 2, 3, 3, 3, 4], 4),
        ([100, 101, 101, 102, 103, 103, 104], 5),

        # --- No consecutive pairs (every gap > 1) ---
        ([1, 3, 5, 7, 9], 1),
        ([10, 20, 30], 1),
        ([-3, -1, 1, 3], 1),

        # --- Negative numbers ---
        ([-1, -2, -3, -4], 4),
        ([-100, -99, -98, 0, 1, 2], 3),
        ([0, -1, -2, 1, 2, 3], 6),
        ([-10, -9, -8, -7, -5, -4, -3], 4),

        # --- Cross zero ---
        ([-2, -1, 0, 1, 2], 5),
        ([-1, 0, 1], 3),
        ([0, 1, -1], 3),

        # --- Large gaps ---
        ([1, 2, 3, 1000, 1001, 1002, 1003], 4),
        ([-1_000_000_000, 0, 1_000_000_000], 1),

        # --- Two separate runs of equal length ---
        ([1, 2, 3, 10, 11, 12], 3),
        ([1, 2, 3, 4, 10, 11, 12, 13], 4),

        # --- One long run, one short run ---
        ([1, 2, 3, 4, 5, 100, 101], 5),
        ([1, 2, 100, 101, 102, 103], 4),

        # --- Boundary values ---
        ([-10**9], 1),
        ([10**9], 1),
        ([-10**9, -10**9 + 1, -10**9 + 2], 3),
        ([10**9 - 2, 10**9 - 1, 10**9], 3),

        # --- Sequence at max range ---
        ([10**9 - 1, 10**9], 2),

        # --- Repeated values plus one long run ---
        ([1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 5),

        # --- Unsorted with interleaved runs ---
        ([4, 0, -4, 1, -3, 2, -2, 3, -1], 9),
        # -> -4,-3,-2,-1,0,1,2,3,4

        # --- Almost consecutive with one break ---
        ([1, 2, 3, 5, 6, 7], 3),
        ([1, 2, 3, 4, 6, 7, 8, 9], 4),

        # --- Maximum-ish input, all distinct consecutive ---
        (list(range(0, 1000)), 1000),
        (list(range(-500, 500)), 1000),
    ],
)
def test_longest_consecutive_returns_expected(nums, expected):
    assert solution_module.solve(nums) == expected


def test_returns_int():
    assert isinstance(solution_module.solve([1, 2, 3]), int)
    assert isinstance(solution_module.solve([]), int)


def test_empty_input_returns_zero():
    assert solution_module.solve([]) == 0


def test_does_not_mutate_input_order():
    """The solution may sort a copy, but must not reorder the caller's list."""
    original = [3, 1, 2, 5, 4]
    snapshot = list(original)
    solution_module.solve(original)
    assert original == snapshot


def test_does_not_mutate_input_contents():
    """No elements added, removed, or changed."""
    original = [1, 2, 2, 3, -1, 0]
    snapshot = list(original)
    solution_module.solve(original)
    assert sorted(original) == sorted(snapshot)


def test_longest_is_not_affected_by_duplicates():
    """Adding duplicates must not change the answer."""
    base = [1, 2, 3, 10, 11, 12, 13]
    with_dups = base + [1, 2, 3, 10, 11, 12, 13, 13, 13]
    assert solution_module.solve(base) == solution_module.solve(with_dups)


def test_longest_run_wins_over_shorter_runs():
    nums = [1, 2, 3, 4, 5, 6, 100, 101, 102]
    assert solution_module.solve(nums) == 6


def test_handles_large_input_in_linear_time():
    """Sanity: a 100k-element input should not blow up (O(n) expected)."""
    random.seed(0)
    nums = list(range(100_000))
    random.shuffle(nums)
    assert solution_module.solve(nums) == 100_000


# ---------------------------------------------------------------------------
# Benchmark (required by algorithms/test-all.py)
# ---------------------------------------------------------------------------

def _candidate_functions():
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if function.__module__ == solution_module.__name__
        and (name == "solve" or name.startswith("solve_"))
    ]


def _build_case(size, case):
    """Return a list of ints of the given size and shape."""
    random.seed(42 + size)
    if case == "consecutive":
        # Fully consecutive, shuffled -> worst case for the O(n) hash-set method
        values = list(range(size))
        random.shuffle(values)
        return values
    if case == "random":
        # Random ints -> mostly short runs
        return [random.randrange(-1_000_000, 1_000_001) for _ in range(size)]
    if case == "no-pairs":
        # Every element isolated -> answer is 1
        return [2 * i for i in range(size)]
    raise ValueError(f"unknown case: {case}")


def run_benchmark():
    sizes = [100, 1_000, 5_000, 10_000]
    cases = ["consecutive", "random", "no-pairs"]
    repetitions = 3
    candidates = _candidate_functions()

    print("\nBenchmark genere automatiquement (Longest Consecutive Sequence)")
    print(f"{'Fonction':>24} | {'n':>8} | {'cas':>12} | {'Temps moyen (ms)':>18}")
    print("-" * 76)

    for function in candidates:
        for size in sizes:
            for case in cases:
                nums = _build_case(size, case)
                try:
                    function(nums)  # warm-up
                    start = time.perf_counter()
                    for _ in range(repetitions):
                        function(nums)
                    elapsed_ms = (time.perf_counter() - start) * 1_000 / repetitions
                except (AttributeError, IndexError, TypeError, ValueError, RecursionError) as error:
                    print(f"{function.__name__:>24} | {size:>8,} | {case:>12} | ignoree: {error}")
                    continue
                print(f"{function.__name__:>24} | {size:>8,} | {case:>12} | {elapsed_ms:>18.4f}")

    if not candidates:
        print("Aucune fonction solve ou solve_* trouvee.")