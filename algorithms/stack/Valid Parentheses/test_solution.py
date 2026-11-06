import importlib.util
import inspect
import itertools
import time
from pathlib import Path

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_valid_parentheses_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)
is_valid_parentheses = solution_module.is_valid_parentheses


def _candidate_solutions():
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if function.__module__ == solution_module.__name__
        and (name == "solve" or name.startswith("solve_hint_"))
    ]


def reference_is_valid(value):
    """Independent stack-based oracle used for the exhaustive comparison."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for character in value:
        if character in "([{":
            stack.append(character)
        elif not stack or stack.pop() != pairs[character]:
            return False
    return not stack


def test_valid_parentheses_statement_examples():
    assert is_valid_parentheses("[]") is True
    assert is_valid_parentheses("([{}])") is True
    assert is_valid_parentheses("[(])") is False


def test_valid_parentheses_accepts_balanced_brackets():
    assert is_valid_parentheses("()[]{}") is True
    assert is_valid_parentheses("{[()]}") is True
    assert is_valid_parentheses("({[]})[]{()}") is True
    assert is_valid_parentheses("((()))") is True


def test_valid_parentheses_rejects_mismatched_types():
    assert is_valid_parentheses("(]") is False
    assert is_valid_parentheses("{)") is False
    assert is_valid_parentheses("[}") is False


def test_valid_parentheses_rejects_misordered_brackets():
    assert is_valid_parentheses("([)]") is False
    assert is_valid_parentheses("{[}]") is False
    assert is_valid_parentheses("[(])") is False


def test_valid_parentheses_rejects_unclosed_openers():
    assert is_valid_parentheses("(") is False
    assert is_valid_parentheses("((") is False
    assert is_valid_parentheses("({[") is False
    assert is_valid_parentheses("()(") is False


def test_valid_parentheses_rejects_unmatched_closers():
    assert is_valid_parentheses(")") is False
    assert is_valid_parentheses("())") is False
    assert is_valid_parentheses("]()") is False
    assert is_valid_parentheses("}{") is False


def test_valid_parentheses_odd_length_is_always_invalid():
    for value in ("(", "()(", "[]{", "({[]})]"):
        assert len(value) % 2 == 1
        assert is_valid_parentheses(value) is False


def test_valid_parentheses_accepts_empty_string():
    assert solution_module.solve("") is True


def test_valid_parentheses_max_constraint_size():
    # Constraint: 1 <= s.length <= 1000
    nested = "(" * 500 + ")" * 500
    flat = "()" * 500
    broken = "(" * 500 + "]" + ")" * 499
    assert len(nested) == len(flat) == len(broken) == 1000
    assert is_valid_parentheses(nested) is True
    assert is_valid_parentheses(flat) is True
    assert is_valid_parentheses(broken) is False


def test_valid_parentheses_exhaustive_short_inputs():
    alphabet = "()[]{}"
    candidates = _candidate_solutions()
    for length in range(8):
        for characters in itertools.product(alphabet, repeat=length):
            value = "".join(characters)
            expected = reference_is_valid(value)
            assert is_valid_parentheses(value) == expected, repr(value)
            for candidate in candidates:
                assert candidate(value) == expected, f"{candidate.__name__}({value!r})"


def run_benchmark():
    candidates = _candidate_solutions()
    print("\nBenchmark: Valid Parentheses")
    print(f"{'Solution':>24} | {'Longueur':>10} | {'Temps (ms)':>12}")
    print("-" * 54)
    for candidate in candidates:
        for size in (1_000, 10_000, 100_000):
            value = "(" * size + ")" * size
            started = time.perf_counter()
            for _ in range(3):
                result = candidate(value)
            elapsed_ms = (time.perf_counter() - started) * 1_000 / 3
            assert result is True
            print(f"{candidate.__name__:>24} | {len(value):>10,} | {elapsed_ms:>12.4f}")


if __name__ == "__main__":
    run_benchmark()
