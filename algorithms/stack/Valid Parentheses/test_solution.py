import importlib.util
import itertools
from pathlib import Path
import time

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_valid_parentheses_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)
is_valid_parentheses = solution_module.is_valid_parentheses


def test_valid_parentheses_accepts_balanced_brackets():
    assert is_valid_parentheses("()[]{}") is True
    assert is_valid_parentheses("{[()]}") is True


def test_valid_parentheses_rejects_mismatched_or_misordered_brackets():
    assert is_valid_parentheses("(]") is False
    assert is_valid_parentheses("([)]") is False
    assert is_valid_parentheses("((") is False


def test_valid_parentheses_accepts_empty_string():
    assert solution_module.solve("") is True


def test_valid_parentheses_exhaustive_short_inputs():
    alphabet = "()[]{}"
    for length in range(8):
        for characters in itertools.product(alphabet, repeat=length):
            value = "".join(characters)
            stack = []
            expected = True
            pairs = {")": "(", "]": "[", "}": "{"}
            for character in value:
                if character in "([{":
                    stack.append(character)
                elif not stack or stack.pop() != pairs[character]:
                    expected = False
                    break
            expected = expected and not stack
            assert is_valid_parentheses(value) == expected, repr(value)


def run_benchmark():
    print("\nBenchmark: Valid Parentheses")
    print(f"{'Longueur':>10} | {'Temps (ms)':>12}")
    print("-" * 26)
    for size in (1_000, 10_000, 100_000):
        value = "(" * size + ")" * size
        started = time.perf_counter()
        for _ in range(3):
            is_valid_parentheses(value)
        elapsed_ms = (time.perf_counter() - started) * 1_000 / 3
        print(f"{len(value):>10,} | {elapsed_ms:>12.4f}")