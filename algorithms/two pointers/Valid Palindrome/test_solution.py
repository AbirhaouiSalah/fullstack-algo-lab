import importlib.util
import inspect
import random
import time
from pathlib import Path

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("two_pointers_valid_palindrome", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)


def _candidates():
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if name == "solve" or name.startswith("solve_hint_")
    ]


def _reference(value: str) -> bool:
    normalized = "".join(character.lower() for character in value if character.isalnum())
    return normalized == normalized[::-1]


def _assert_candidates(value: str, expected: bool) -> None:
    for candidate in _candidates():
        actual = candidate(value)
        if actual is not None:
            assert actual == expected, f"{candidate.__name__}({value!r})"


def test_valid_palindrome_examples_and_edge_cases():
    for value in (
        "A man, a plan, a canal: Panama",
        "race a car",
        " ",
        "",
        "0P",
        ".,",
        "ab_a",
        "No 'x' in Nixon",
    ):
        _assert_candidates(value, _reference(value))


def test_valid_palindrome_seeded_random_inputs():
    rng = random.Random(103)
    alphabet = "abcXYZ019 ,.!?_-"
    for _ in range(300):
        value = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 100)))
        _assert_candidates(value, _reference(value))


def run_benchmark():
    print("\nBenchmark: Valid Palindrome")
    print(f"{'Solver':>20} | {'Characters':>12} | {'Time (ms)':>12}")
    print("-" * 50)
    for candidate in _candidates():
        for size in (1_000, 10_000, 100_000):
            value = "a" * size
            started = time.perf_counter()
            result = candidate(value)
            elapsed_ms = (time.perf_counter() - started) * 1_000
            if result is None:
                print(f"{candidate.__name__:>20} | {size:>12,} | {'incomplete':>12}")
                break
            assert result is True
            print(f"{candidate.__name__:>20} | {size:>12,} | {elapsed_ms:>12.4f}")
