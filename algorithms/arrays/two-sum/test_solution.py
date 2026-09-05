import random
import time
from pathlib import Path
import importlib.util


solution_path = Path(__file__).with_name("solution.py")
solution_spec = importlib.util.spec_from_file_location("two_sum_solution", solution_path)
if solution_spec is None or solution_spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(solution_spec)
solution_spec.loader.exec_module(solution_module)

two_sum = solution_module.two_sum
two_sum_brute_force = solution_module.two_sum_brute_force


def test_example_1():
    assert two_sum([3, 4, 5, 6], 7) == [0, 1]


def test_example_2():
    assert two_sum([4, 5, 6], 10) == [0, 2]


def test_example_3_duplicate_values():
    assert two_sum([5, 5], 10) == [0, 1]


def test_negative_values():
    assert two_sum([-3, 4, 8, -1], 5) == [0, 2]


def test_returns_indices_in_ascending_order():
    assert two_sum([10, 2, 7, 3], 5) == [1, 3]


def test_generated_cases_match_brute_force():
    generator = random.Random(42)

    for size in (2, 5, 25, 100):
        nums = [generator.randint(-10_000, 10_000) for _ in range(size)]
        first_index, second_index = sorted(generator.sample(range(size), 2))
        nums[first_index] = 123_456
        nums[second_index] = -54_321
        target = nums[first_index] + nums[second_index]

        assert two_sum(nums, target) == two_sum_brute_force(nums, target)


def run_benchmark():
    sizes = [100, 1_000, 5_000, 10_000]
    repetitions = 3
    implementations = [
        ("Hash map", two_sum, "O(n)"),
        ("Brute force", two_sum_brute_force, "O(n²)"),
    ]
    results = {name: [] for name, _, _ in implementations}
    random_generator = random.Random(42)

    for size in sizes:
        nums = [random_generator.randrange(-1_000_000, 1_000_001) for _ in range(size)]
        nums[-2:] = [123_456, -54_321]
        target = nums[-2] + nums[-1]

        for name, solver, _ in implementations:
            solver(nums, target)
            start = time.perf_counter()
            for _ in range(repetitions):
                solver(nums, target)
            elapsed_ms = (time.perf_counter() - start) * 1_000 / repetitions
            results[name].append(elapsed_ms)

    print("\nComparaison des performances: Two Sum")
    header = " | ".join(
        [f"{'Input n':>10}"] + [f"{name:>14}" for name, _, _ in implementations]
    )
    print(header)
    print("-" * len(header))
    for index, size in enumerate(sizes):
        timings = " | ".join(
            f"{results[name][index]:>14.4f}" for name, _, _ in implementations
        )
        print(f"{size:>10,} | {timings}")

    print("\nResume de complexite")
    print(f"{'Implementation':>16} | {'Complexite':>12} | {'Temps a n=10,000 (ms)':>22}")
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