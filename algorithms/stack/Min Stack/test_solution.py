import importlib.util
import random
import time
from pathlib import Path

import pytest

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_min_stack_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)

INT_MIN = -(2**31)
INT_MAX = 2**31 - 1

ALL_IMPLEMENTATIONS = [
    solution_module.MinStack,
    solution_module.MinStackHint1,
    solution_module.MinStackHint2,
    solution_module.MinStackHint3,
]
# Hint 1 is O(n) per get_min, so it is excluded from large-scale tests.
FAST_IMPLEMENTATIONS = [
    solution_module.MinStack,
    solution_module.MinStackHint2,
    solution_module.MinStackHint3,
]


@pytest.fixture(params=ALL_IMPLEMENTATIONS, ids=lambda cls: cls.__name__)
def stack(request):
    return request.param()


def test_statement_example(stack):
    stack.push(1)
    stack.push(2)
    stack.push(0)
    assert stack.get_min() == 0
    stack.pop()
    assert stack.top() == 2
    assert stack.get_min() == 1


def test_single_element(stack):
    stack.push(42)
    assert stack.top() == 42
    assert stack.get_min() == 42


def test_single_element_push_then_pop_leaves_stack_empty(stack):
    stack.push(7)
    stack.pop()
    with pytest.raises(IndexError):
        stack.top()
    with pytest.raises(IndexError):
        stack.get_min()


def test_duplicate_minimums_survive_one_pop(stack):
    stack.push(2)
    stack.push(1)
    stack.push(1)
    assert stack.get_min() == 1
    stack.pop()
    assert stack.get_min() == 1  # the second 1 is still there
    stack.pop()
    assert stack.get_min() == 2


def test_all_equal_values(stack):
    for _ in range(5):
        stack.push(3)
    for _ in range(5):
        assert stack.get_min() == 3
        assert stack.top() == 3
        stack.pop()


def test_strictly_decreasing_values(stack):
    for value in (5, 4, 3, 2, 1):
        stack.push(value)
        assert stack.get_min() == value
    for expected in (1, 2, 3, 4, 5):
        assert stack.get_min() == expected
        stack.pop()


def test_strictly_increasing_values(stack):
    for value in (1, 2, 3, 4, 5):
        stack.push(value)
        assert stack.get_min() == 1
    for expected_top in (5, 4, 3, 2, 1):
        assert stack.top() == expected_top
        assert stack.get_min() == 1
        stack.pop()


def test_minimum_is_restored_after_popping_it(stack):
    stack.push(5)
    stack.push(3)
    stack.push(8)
    stack.push(1)
    stack.push(9)
    assert stack.get_min() == 1
    stack.pop()  # 9
    assert stack.get_min() == 1
    stack.pop()  # 1
    assert stack.get_min() == 3
    stack.pop()  # 8
    assert stack.get_min() == 3
    stack.pop()  # 3
    assert stack.get_min() == 5


def test_negative_and_zero_values(stack):
    for value in (0, -1, -5, 3, -5, 0):
        stack.push(value)
    assert stack.get_min() == -5
    stack.pop()  # 0
    stack.pop()  # -5 (one of two)
    assert stack.get_min() == -5
    stack.pop()  # 3
    stack.pop()  # -5 (second)
    assert stack.get_min() == -1


def test_int32_bounds(stack):
    stack.push(INT_MAX)
    assert stack.get_min() == INT_MAX
    stack.push(INT_MIN)
    assert stack.get_min() == INT_MIN
    assert stack.top() == INT_MIN
    stack.push(INT_MAX)
    assert stack.get_min() == INT_MIN
    stack.pop()
    stack.pop()
    assert stack.top() == INT_MAX
    assert stack.get_min() == INT_MAX


def test_top_does_not_remove_elements(stack):
    stack.push(1)
    stack.push(2)
    assert stack.top() == 2
    assert stack.top() == 2
    assert stack.get_min() == 1
    assert stack.get_min() == 1


def test_reuse_after_emptying(stack):
    stack.push(1)
    stack.push(2)
    stack.pop()
    stack.pop()
    stack.push(10)
    assert stack.top() == 10
    assert stack.get_min() == 10  # no stale minimum from the previous content


def test_operations_on_empty_stack_raise(stack):
    with pytest.raises(IndexError):
        stack.pop()
    with pytest.raises(IndexError):
        stack.top()
    with pytest.raises(IndexError):
        stack.get_min()


def test_randomized_against_brute_force_oracle(stack):
    rng = random.Random(1234)
    oracle: list[int] = []
    for _ in range(3_000):
        operation = rng.choice(("push", "push", "pop", "top", "min"))
        if operation == "push" or not oracle:
            value = rng.choice((INT_MIN, INT_MAX, 0, rng.randint(-5, 5)))
            stack.push(value)
            oracle.append(value)
        elif operation == "pop":
            stack.pop()
            oracle.pop()
        elif operation == "top":
            assert stack.top() == oracle[-1]
        else:
            assert stack.get_min() == min(oracle)


@pytest.mark.parametrize("implementation", FAST_IMPLEMENTATIONS, ids=lambda cls: cls.__name__)
def test_max_call_count_from_constraints(implementation):
    # Constraint: at most 3 * 10^4 calls.
    stack = implementation()
    for value in range(15_000, 0, -1):
        stack.push(value)
    assert stack.get_min() == 1
    for expected_min in range(1, 15_001):
        assert stack.get_min() == expected_min
        stack.pop()


def _build_full_stack(implementation, size):
    stack = implementation()
    for value in range(size, 0, -1):
        stack.push(value)
    return stack


def _time_get_min(implementation, size, calls=1_000):
    stack = _build_full_stack(implementation, size)
    started = time.perf_counter()
    for _ in range(calls):
        stack.get_min()
    return (time.perf_counter() - started) * 1_000


def _time_push_pop(implementation, size, cycles=1_000):
    stack = _build_full_stack(implementation, size)
    started = time.perf_counter()
    for value in range(cycles):
        stack.push(value)
        stack.pop()
    return (time.perf_counter() - started) * 1_000


def _print_table(title, measure):
    names = [cls.__name__ for cls in ALL_IMPLEMENTATIONS]
    print(f"\n{title}")
    print(f"{'Taille':>10} | " + " | ".join(f"{name + ' (ms)':>20}" for name in names))
    print("-" * (13 + 23 * len(names)))
    for size in (1_000, 10_000, 30_000):
        timings = [measure(cls, size) for cls in ALL_IMPLEMENTATIONS]
        print(f"{size:>10,} | " + " | ".join(f"{t:>20.4f}" for t in timings))


def run_benchmark():
    _print_table("Benchmark: Min Stack - get_min x1000 sur pile pleine", _time_get_min)
    _print_table("Benchmark: Min Stack - push+pop x1000 sur pile pleine", _time_push_pop)


if __name__ == "__main__":
    run_benchmark()