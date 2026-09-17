import importlib.util
from pathlib import Path

import pytest


solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("climbing_stairs_solution", solution_path)
if spec is None or spec.loader is None:
	raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)


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
	assert solution_module.solve(steps) == expected


def test_climb_stairs_follows_fibonacci_recurrence():
	results = [solution_module.solve(steps) for steps in range(1, 46)]

	assert results[0] == 1
	assert results[1] == 2
	for index in range(2, len(results)):
		assert results[index] == results[index - 1] + results[index - 2]
