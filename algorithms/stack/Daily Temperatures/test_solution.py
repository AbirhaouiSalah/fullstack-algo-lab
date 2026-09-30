import importlib.util
import random
import time
from pathlib import Path

import pytest

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_daily_temperatures_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)

ALL_IMPLEMENTATIONS = [
    solution_module.daily_temperatures,
    solution_module.solve_hint_1,
    solution_module.solve_hint_2,
    solution_module.solve_hint_3,
    solution_module.solve_bonus_jump_pointers,
]
# Hint 1 is O(n^2) in the worst case, so it is excluded from large-scale tests.
FAST_IMPLEMENTATIONS = [
    function for function in ALL_IMPLEMENTATIONS if function is not solution_module.solve_hint_1
]


@pytest.fixture(params=ALL_IMPLEMENTATIONS, ids=lambda function: function.__name__)
def compute(request):
    return request.param


def reference(temperatures):
    """Independent oracle: literal translation of the statement."""
    result = []
    for day, temperature in enumerate(temperatures):
        wait = 0
        for offset, future in enumerate(temperatures[day + 1 :], start=1):
            if future > temperature:
                wait = offset
                break
        result.append(wait)
    return result


def test_statement_examples(compute):
    assert compute([30, 38, 30, 36, 35, 40, 28]) == [1, 4, 1, 2, 1, 0, 0]
    assert compute([22, 21, 20]) == [0, 0, 0]


def test_solve_alias_matches_main_solution():
    assert solution_module.solve([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]


def test_classic_leetcode_examples(compute):
    assert compute([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert compute([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert compute([30, 60, 90]) == [1, 1, 0]


def test_single_day(compute):
    assert compute([50]) == [0]


def test_two_days(compute):
    assert compute([50, 60]) == [1, 0]
    assert compute([60, 50]) == [0, 0]
    assert compute([50, 50]) == [0, 0]


def test_all_equal_temperatures_never_warmer(compute):
    assert compute([70] * 6) == [0] * 6


def test_strictly_increasing(compute):
    assert compute([1, 2, 3, 4, 5]) == [1, 1, 1, 1, 0]


def test_strictly_decreasing(compute):
    assert compute([5, 4, 3, 2, 1]) == [0, 0, 0, 0, 0]


def test_warmer_day_must_be_strictly_warmer(compute):
    # equal temperature does not count as warmer
    assert compute([50, 50, 51]) == [2, 1, 0]
    assert compute([50, 50, 50, 49, 51]) == [4, 3, 2, 1, 0]


def test_plateaus_between_peaks(compute):
    assert compute([40, 40, 40, 60, 60, 50, 70]) == [3, 2, 1, 3, 2, 1, 0]


def test_last_element_is_always_zero(compute):
    for temperatures in ([1, 2, 3], [3, 2, 1], [5], [1, 100]):
        assert compute(temperatures)[-1] == 0


def test_temperature_bounds_from_constraints(compute):
    assert compute([1, 100]) == [1, 0]
    assert compute([100, 1]) == [0, 0]
    assert compute([100, 100, 100]) == [0, 0, 0]
    assert compute([1, 1, 1, 100]) == [3, 2, 1, 0]


def test_zigzag(compute):
    assert compute([50, 60, 50, 60, 50, 60]) == [1, 0, 1, 0, 1, 0]


def test_far_away_warmer_day(compute):
    assert compute([50, 40, 40, 40, 40, 51]) == [5, 4, 3, 2, 1, 0]


def test_nested_valleys(compute):
    # deep stack popped all at once by the final peak
    assert compute([90, 80, 70, 60, 50, 100]) == [5, 4, 3, 2, 1, 0]


def test_result_has_same_length_and_int_items(compute):
    temperatures = [30, 38, 30, 36, 35, 40, 28]
    result = compute(temperatures)
    assert isinstance(result, list)
    assert len(result) == len(temperatures)
    assert all(isinstance(value, int) for value in result)


def test_input_list_is_not_mutated(compute):
    temperatures = [30, 38, 30, 36, 35, 40, 28]
    snapshot = list(temperatures)
    compute(temperatures)
    assert temperatures == snapshot


def test_exhaustive_small_inputs(compute):
    # every sequence of length <= 6 over a small temperature alphabet
    import itertools

    for length in range(1, 7):
        for temperatures in itertools.product((1, 2, 3, 100), repeat=length):
            values = list(temperatures)
            assert compute(values) == reference(values), values


def test_randomized_against_brute_force_oracle(compute):
    rng = random.Random(4242)
    for _ in range(300):
        size = rng.randint(1, 60)
        temperatures = [rng.randint(1, 100) for _ in range(size)]
        assert compute(temperatures) == reference(temperatures), temperatures


@pytest.mark.parametrize("function", FAST_IMPLEMENTATIONS, ids=lambda function: function.__name__)
def test_max_size_from_constraints(function):
    # Constraint: 1 <= temperatures.length <= 100_000
    size = 100_000

    assert function([50] * size) == [0] * size

    # one late hot day: answers count down from 99_999 to 1, then 0
    spike = [1] * (size - 1) + [100]
    assert function(spike) == list(range(size - 1, 0, -1)) + [0]

    # sawtooth 1..100: each day waits exactly one day, except the peaks
    sawtooth = [(i % 100) + 1 for i in range(size)]
    result = function(sawtooth)
    assert len(result) == size
    assert result[0] == 1
    assert result == reference_fast(sawtooth)


def reference_fast(temperatures):
    """O(n) oracle (next greater element, right to left) for large inputs."""
    size = len(temperatures)
    result = [0] * size
    stack = []
    for index in range(size - 1, -1, -1):
        while stack and temperatures[stack[-1]] <= temperatures[index]:
            stack.pop()
        result[index] = stack[-1] - index if stack else 0
        stack.append(index)
    return result


def _non_increasing(size):
    # worst case for the brute force: every day scans the whole remainder
    return [100 - (index * 99) // max(size - 1, 1) for index in range(size)]


def _time_compute(function, size, runs=3):
    temperatures = _non_increasing(size)
    started = time.perf_counter()
    for _ in range(runs):
        function(temperatures)
    return (time.perf_counter() - started) * 1_000 / runs


def run_benchmark():
    names = [function.__name__ for function in ALL_IMPLEMENTATIONS]
    print("\nBenchmark: Daily Temperatures - sequence non croissante (pire cas brute force)")
    print(f"{'Taille':>10} | " + " | ".join(f"{name + ' (ms)':>26}" for name in names))
    print("-" * (13 + 29 * len(names)))
    for size in (1_000, 5_000, 10_000):
        timings = [_time_compute(function, size) for function in ALL_IMPLEMENTATIONS]
        print(f"{size:>10,} | " + " | ".join(f"{t:>26.4f}" for t in timings))


if __name__ == "__main__":
    run_benchmark()
