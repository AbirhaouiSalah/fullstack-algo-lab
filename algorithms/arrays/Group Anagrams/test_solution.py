import importlib.util
import random
import time
from pathlib import Path

solution_path = Path(__file__).with_name("solution.py")
solution_spec = importlib.util.spec_from_file_location("group_anagrams_solution", solution_path)
if solution_spec is None or solution_spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(solution_spec)
solution_spec.loader.exec_module(solution_module)

implementations = [
    solution_module.solve_hint_1,
#    solution_module.solve_hint_2,
#    solution_module.solve_hint_3,
]


def normalize(groups):
    return sorted(sorted(group) for group in groups)


def test_example_1():
    expected = [["hat"], ["act", "cat"], ["pots", "stop", "tops"]]
    for solve in implementations:
        assert normalize(solve(["act", "pots", "tops", "cat", "stop", "hat"])) == normalize(
            expected
        )


def test_example_2():
    for solve in implementations:
        assert solve(["x"]) == [["x"]]


def test_example_3_empty_string():
    for solve in implementations:
        assert solve([""]) == [[""]]


def test_repeated_letters_and_empty_strings():
    values = ["", "", "a", "a", "aa", "a", "baa", "aba"]
    expected = [["", ""], ["a", "a", "a"], ["aa"], ["aba", "baa"]]
    for solve in implementations:
        assert normalize(solve(values)) == normalize(expected)


def test_generated_cases_match_all_implementations():
    generator = random.Random(42)
    values = ["".join(generator.choices("abcde", k=generator.randrange(0, 12))) for _ in range(500)]
    expected = normalize(implementations[0](values))

    for solve in implementations[1:]:
        assert normalize(solve(values)) == expected


def run_benchmark():
    sizes = [100, 1_000, 5_000, 10_000]
    repetitions = 3
    random_generator = random.Random(42)
    results = {solve.__name__: [] for solve in implementations}

    for size in sizes:
        values = [
            "".join(random_generator.choices("abcdefghijklmnopqrstuvwxyz", k=10))
            for _ in range(size)
        ]
        for solve in implementations:
            solve(values)
            start = time.perf_counter()
            for _ in range(repetitions):
                solve(values)
            elapsed_ms = (time.perf_counter() - start) * 1_000 / repetitions
            results[solve.__name__].append(elapsed_ms)

    print("\nComparaison des performances: Group Anagrams")
    header = " | ".join(
        [f"{'Input n':>10}"] + [f"{solve.__name__:>14}" for solve in implementations]
    )
    print(header)
    print("-" * len(header))
    for index, size in enumerate(sizes):
        timings = " | ".join(
            f"{results[solve.__name__][index]:>14.4f}" for solve in implementations
        )
        print(f"{size:>10,} | {timings}")

    print("\nResume de complexite")
    print(f"{'Implementation':>16} | {'Complexite':>12} | {'Temps a n=10,000 (ms)':>23}")
    print("-" * 58)
    complexities = ["O(n * k log k)", "O(n * k)", "O(n * k)"]
    for solve, complexity in zip(implementations, complexities):
        print(f"{solve.__name__:>16} | {complexity:>12} | {results[solve.__name__][-1]:>23.4f}")
