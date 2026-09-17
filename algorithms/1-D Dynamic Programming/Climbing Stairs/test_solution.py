import importlib.util
import sys
from pathlib import Path

import pytest


solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("climbing_stairs_solution", solution_path)

if spec is None or spec.loader is None:
    pytest.fail(f"Cannot load solution from {solution_path}", pytrace=False)

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
        (45, 1_836_311_903),
    ],
)
def test_climb_stairs_returns_expected_number_of_ways(steps, expected):
    assert solve(steps) == expected


def test_climb_stairs_follows_fibonacci_recurrence():
    results = [solve(steps) for steps in range(1, 46)]

    assert results[0] == 1
    assert results[1] == 2
    for index in range(2, len(results)):
        assert results[index] == results[index - 1] + results[index - 2]