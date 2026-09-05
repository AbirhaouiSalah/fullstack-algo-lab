import importlib.util
import random
import time
from pathlib import Path

solution_path = Path(__file__).with_name("solution.py")
solution_spec = importlib.util.spec_from_file_location("top_k_solution", solution_path)
if solution_spec is None or solution_spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(solution_spec)
solution_spec.loader.exec_module(solution_module)

solve_hint_1 = solution_module.solve_hint_1
solve_hint_2 = solution_module.solve_hint_2
solve_hint_3 = solution_module.solve_hint_3


def batch(args0, args1, args2):
    case = args2
    if case == 0:
        return solve_hint_1(args0, args1)
    if case == 1:
        return solve_hint_2(args0, args1)
    if case == 2:
        return solve_hint_3(args0, args1)
    raise ValueError(f"Invalid case number: {case}")


def test_batch_hint_1():
    result = batch([1, 1, 1, 2, 2, 3], 2, 0)

    assert sorted(result) == [1, 2]


def test_example_1():
    result = batch([1, 2, 2, 3, 3, 3], 2, 0)

    assert sorted(result) == [2, 3]


def test_example_3():
    result = batch([1, 1, 1, 2, 2, 3, 3], 1, 0)

    assert sorted(result) == [1]


def test_all_implementations():
    for case in range(3):
        result = batch([1, 1, 1, 2, 2, 3], 2, case)
        assert sorted(result) == [1, 2]


def test_example_2():
    result = batch([7, 7], 1, 0)

    assert sorted(result) == [7]


def run_benchmark():
    sizes = [100, 1_000, 10_000, 50_000, 100_000]
    repetitions = 5
    implementations = [
        ("Tri", solve_hint_1, "O(n log n)"),
        ("Min-heap", solve_hint_2, "O(n log k)"),
        ("Buckets", solve_hint_3, "O(n)"),
    ]
    results = {name: [] for name, _, _ in implementations}
    random_generator = random.Random(42)

    for size in sizes:
        nums = [random_generator.randrange(-1_000, 1_001) for _ in range(size)]
        k = min(10, len(set(nums)))

        for name, solver, _ in implementations:
            solver(nums, k)
            start = time.perf_counter()
            for _ in range(repetitions):
                solver(nums, k)
            elapsed_ms = (time.perf_counter() - start) * 1_000 / repetitions
            results[name].append(elapsed_ms)

    print("\nComparaison des performances")
    header = " | ".join([f"{'Input n':>10}"] + [f"{name:>14}" for name, _, _ in implementations])
    print(header)
    print("-" * len(header))
    for index, size in enumerate(sizes):
        timings = " | ".join(f"{results[name][index]:>14.4f}" for name, _, _ in implementations)
        print(f"{size:>10,} | {timings}")

    print("\nResume de complexite")
    print(f"{'Implementation':>16} | {'Complexite':>12} | {'Temps a n=100,000 (ms)':>23}")
    print("-" * 58)
    for name, _, complexity in implementations:
        print(f"{name:>16} | {complexity:>12} | {results[name][-1]:>23.4f}")

    print("\nEvolution relative du temps (# = temps maximal observe)")
    max_time = max(max(timings) for timings in results.values())
    for index, size in enumerate(sizes):
        print(f"n={size:>6,}")
        for name, _, _ in implementations:
            elapsed_ms = results[name][index]
            bar_length = max(1, round(elapsed_ms / max_time * 40))
            print(f"  {name:>8}: {'#' * bar_length} {elapsed_ms:.4f} ms")
