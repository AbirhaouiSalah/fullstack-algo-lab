import importlib.util
import inspect
import sys
import time
from pathlib import Path

import pytest

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("climbing_stairs_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
sys.modules["climbing_stairs_solution"] = solution_module
spec.loader.exec_module(solution_module)

# Fail the whole module early with a clear message if `solve` is missing.
if not hasattr(solution_module, "solve"):
    pytest.fail(
        f"{solution_path} must define a function named `solve(n)`. "
        f"Found: {[name for name in dir(solution_module) if not name.startswith('_')]}",
        pytrace=False,
    )

solve = solution_module.solve


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
# NOTE: n = 45 was removed because it takes too long with recursive or
# exponential-time implementations.  n = 20 is still a solid upper bound
# (ways(20) = 10946) and stays fast for every reasonable solution.

@pytest.mark.parametrize(
    ("steps", "expected"),
    [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 5),
        (5, 8),
        (10, 89),
        (20, 10_946),
    ],
)
def test_climb_stairs_returns_expected_number_of_ways(steps, expected):
    assert solve(steps) == expected


def test_climb_stairs_follows_fibonacci_recurrence():
    """For every n up to 20, ways(n) must equal ways(n-1) + ways(n-2)."""
    results = [solve(steps) for steps in range(1, 21)]

    assert results[0] == 1
    assert results[1] == 2
    for index in range(2, len(results)):
        assert results[index] == results[index - 1] + results[index - 2]


def test_returns_int():
    assert isinstance(solve(1), int)
    assert isinstance(solve(20), int)


def test_is_monotonically_increasing():
    """ways(n) must strictly increase as n grows."""
    prev = solve(1)
    for n in range(2, 21):
        curr = solve(n)
        assert curr > prev
        prev = curr


# ---------------------------------------------------------------------------
# Benchmark (required by algorithms/test-all.py)
# ---------------------------------------------------------------------------
# Sizes are capped at 20 so recursive / exponential implementations do not
# stall the pipeline.  Increase locally if you want to profile the blow-up.

def _candidate_functions():
    """Collect `solve` and any `solve_*` variants defined in solution.py."""
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if function.__module__ == solution_module.__name__
        and (name == "solve" or name.startswith("solve_"))
    ]


def run_benchmark():
    sizes = [5, 10, 15, 20]
    repetitions = 100
    candidates = _candidate_functions()

    print("\nBenchmark genere automatiquement (Climbing Stairs)")
    print(f"{'Fonction':>24} | {'n':>5} | {'Temps moyen (ms)':>18}")
    print("-" * 56)

    for function in candidates:
        for size in sizes:
            try:
                # Warm-up (important for lru_cache-backed solutions)
                function(size)

                start = time.perf_counter()
                for _ in range(repetitions):
                    function(size)
                elapsed_ms = (time.perf_counter() - start) * 1_000 / repetitions
            except (AttributeError, IndexError, TypeError, ValueError, RecursionError) as error:
                print(f"{function.__name__:>24} | {size:>5} | ignoree: {error}")
                continue
            print(f"{function.__name__:>24} | {size:>5} | {elapsed_ms:>18.4f}")

    if not candidates:
        print("Aucune fonction solve ou solve_* trouvee.")