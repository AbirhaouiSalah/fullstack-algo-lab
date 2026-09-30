import importlib.util
import random
from pathlib import Path
import time

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_min_stack_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)
MinStack = solution_module.MinStack


def test_min_stack_tracks_minimum_as_values_are_pushed_and_popped():
    stack = MinStack()
    stack.push(-2)
    stack.push(0)
    stack.push(-3)

    assert stack.get_min() == -3
    stack.pop()
    assert stack.top() == 0
    assert stack.get_min() == -2


def test_min_stack_handles_duplicate_minimum_values():
    stack = MinStack()
    stack.push(2)
    stack.push(1)
    stack.push(1)
    stack.pop()

    assert stack.get_min() == 1
    stack.pop()
    assert stack.get_min() == 2


def test_min_stack_rejects_reads_and_pop_when_empty():
    stack = MinStack()
    for operation in (stack.pop, stack.top, stack.get_min):
        try:
            operation()
        except IndexError:
            continue
        raise AssertionError("Expected IndexError for an empty MinStack")


def test_min_stack_random_operations_match_list_reference():
    rng = random.Random(421)
    stack = MinStack()
    reference = []

    for _ in range(2_000):
        if not reference or rng.random() < 0.65:
            value = rng.randint(-1_000, 1_000)
            stack.push(value)
            reference.append(value)
        else:
            stack.pop()
            reference.pop()

        assert stack.top() == reference[-1]
        assert stack.get_min() == min(reference)


def run_benchmark():
    print("\nBenchmark: Min Stack (push/top/min/pop)")
    print(f"{'Operations':>12} | {'Temps (ms)':>12}")
    print("-" * 28)
    for size in (1_000, 10_000, 50_000):
        started = time.perf_counter()
        stack = MinStack()
        for value in range(size):
            stack.push(value)
            stack.top()
            stack.get_min()
        for _ in range(size):
            stack.pop()
        elapsed_ms = (time.perf_counter() - started) * 1_000
        print(f"{size * 5:>12,} | {elapsed_ms:>12.4f}")