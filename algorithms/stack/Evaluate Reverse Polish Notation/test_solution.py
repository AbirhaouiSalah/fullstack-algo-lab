import importlib.util
from pathlib import Path
import time

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_rpn_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)
eval_rpn = solution_module.eval_rpn


def test_eval_rpn_evaluates_standard_expressions():
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert solution_module.solve(["4", "13", "5", "/", "+"]) == 6


def test_eval_rpn_truncates_division_toward_zero():
    assert eval_rpn(["-7", "3", "/"]) == -2
    assert eval_rpn(["7", "-3", "/"]) == -2


def test_eval_rpn_preserves_operand_order_for_subtraction():
    assert eval_rpn(["5", "8", "-"]) == -3


def test_eval_rpn_matches_addition_subtraction_and_multiplication_examples():
    examples = [
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
        (["3", "4", "+"], 7),
        (["3", "4", "-"], -1),
        (["-3", "4", "*"], -12),
        (["-8", "3", "/"], -2),
        (["8", "-3", "/"], -2),
    ]
    for tokens, expected in examples:
        assert eval_rpn(tokens) == expected


def run_benchmark():
    print("\nBenchmark: Evaluate Reverse Polish Notation")
    print(f"{'Operations':>12} | {'Tokens':>12} | {'Temps (ms)':>12}")
    print("-" * 42)
    for size in (1_000, 10_000, 50_000):
        tokens = ["1", *(token for _ in range(size) for token in ("1", "+"))]
        started = time.perf_counter()
        result = eval_rpn(tokens)
        elapsed_ms = (time.perf_counter() - started) * 1_000
        assert result == size + 1
        print(f"{size:>12,} | {len(tokens):>12,} | {elapsed_ms:>12.4f}")