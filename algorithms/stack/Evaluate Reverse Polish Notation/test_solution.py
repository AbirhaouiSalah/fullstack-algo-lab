import importlib.util
import random
import time
from pathlib import Path

import pytest

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_eval_rpn_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)

ALL_IMPLEMENTATIONS = [
    solution_module.eval_rpn,
    solution_module.solve_hint_1,
    solution_module.solve_hint_2,
    solution_module.solve_hint_3,
]
# Hint 1 is O(n^2), so it is excluded from large-scale tests.
FAST_IMPLEMENTATIONS = [
    solution_module.eval_rpn,
    solution_module.solve_hint_2,
    solution_module.solve_hint_3,
]


@pytest.fixture(params=ALL_IMPLEMENTATIONS, ids=lambda function: function.__name__)
def evaluate(request):
    return request.param


def test_statement_example(evaluate):
    assert evaluate(["1", "2", "+", "3", "*", "4", "-"]) == 5


def test_solve_alias_matches_main_solution():
    assert solution_module.solve(["4", "13", "5", "/", "+"]) == 6


def test_classic_leetcode_examples(evaluate):
    assert evaluate(["2", "1", "+", "3", "*"]) == 9
    assert evaluate(["4", "13", "5", "/", "+"]) == 6
    assert evaluate(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22


def test_single_number(evaluate):
    assert evaluate(["7"]) == 7
    assert evaluate(["0"]) == 0
    assert evaluate(["-3"]) == -3


def test_each_operator(evaluate):
    assert evaluate(["3", "4", "+"]) == 7
    assert evaluate(["3", "4", "-"]) == -1
    assert evaluate(["3", "4", "*"]) == 12
    assert evaluate(["12", "4", "/"]) == 3


def test_operand_order_matters_for_non_commutative_operators(evaluate):
    # left operand is the one pushed first
    assert evaluate(["10", "3", "-"]) == 7
    assert evaluate(["3", "10", "-"]) == -7
    assert evaluate(["20", "4", "/"]) == 5
    assert evaluate(["4", "20", "/"]) == 0


def test_negative_number_token_is_not_the_minus_operator(evaluate):
    assert evaluate(["-1", "-2", "-"]) == 1  # -1 - (-2)
    assert evaluate(["5", "-3", "+"]) == 2
    assert evaluate(["-5", "-5", "*"]) == 25


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (7, 2, 3),
        (-7, 2, -3),  # floor division would give -4
        (7, -2, -3),  # floor division would give -4
        (-7, -2, 3),
        (1, 2, 0),
        (-1, 2, 0),  # floor division would give -1
        (1, -2, 0),
        (0, 5, 0),
        (0, -5, 0),
        (200, -200, -1),
        (-200, 200, -1),
        (199, 200, 0),
    ],
)
def test_division_truncates_toward_zero(evaluate, left, right, expected):
    assert evaluate([str(left), str(right), "/"]) == expected


def test_no_negative_zero_or_float_leaks(evaluate):
    result = evaluate(["-1", "2", "/"])
    assert result == 0
    assert isinstance(result, int)


def test_operand_bounds_from_constraints(evaluate):
    assert evaluate(["200", "200", "*"]) == 40_000
    assert evaluate(["-200", "-200", "*"]) == 40_000
    assert evaluate(["-200", "200", "*"]) == -40_000
    assert evaluate(["200", "-200", "+"]) == 0
    assert evaluate(["-200", "200", "-"]) == -400


def test_zero_operands(evaluate):
    assert evaluate(["0", "5", "*"]) == 0
    assert evaluate(["0", "5", "+"]) == 5
    assert evaluate(["5", "0", "-"]) == 5
    assert evaluate(["0", "0", "+"]) == 0


def test_deeply_nested_right_operands(evaluate):
    # 1 - (2 - (3 - (4 - 5))) = 3
    assert evaluate(["1", "2", "3", "4", "5", "-", "-", "-", "-"]) == 3


def test_left_leaning_chain(evaluate):
    # ((((1 + 2) + 3) + 4) + 5) = 15
    assert evaluate(["1", "2", "+", "3", "+", "4", "+", "5", "+"]) == 15


def test_big_intermediate_values_stay_exact(evaluate):
    # 200^10 is far beyond 2^53: float-based division would be off.
    big = ["200"] + ["200", "*"] * 9
    exact = 200**10
    assert evaluate(big) == exact
    assert evaluate(big + ["3", "/"]) == exact // 3
    assert evaluate(["-200"] + ["200", "*"] * 9 + ["3", "/"]) == -(exact // 3)


def _random_expression(rng, depth):
    """Return (postfix tokens, exact value) of a random valid expression."""
    if depth == 0 or rng.random() < 0.25:
        value = rng.randint(-200, 200)
        return [str(value)], value

    left_tokens, left_value = _random_expression(rng, depth - 1)
    right_tokens, right_value = _random_expression(rng, depth - 1)
    operator = rng.choice("+-*/")
    if operator == "/" and right_value == 0:
        operator = "+"

    if operator == "+":
        value = left_value + right_value
    elif operator == "-":
        value = left_value - right_value
    elif operator == "*":
        value = left_value * right_value
    else:
        quotient = abs(left_value) // abs(right_value)
        value = quotient if (left_value < 0) == (right_value < 0) else -quotient

    return left_tokens + right_tokens + [operator], value


def test_randomized_against_expression_tree_oracle(evaluate):
    rng = random.Random(2024)
    for _ in range(500):
        tokens, expected = _random_expression(rng, depth=6)
        assert evaluate(tokens) == expected, tokens


def test_input_list_is_not_mutated(evaluate):
    tokens = ["1", "2", "+", "3", "*", "4", "-"]
    snapshot = list(tokens)
    evaluate(tokens)
    assert tokens == snapshot


@pytest.mark.parametrize("function", FAST_IMPLEMENTATIONS, ids=lambda function: function.__name__)
def test_max_token_count_from_constraints(function):
    # Constraint: 1 <= tokens.length <= 10_000
    # Left-leaning chain: 1 + 1 + ... (5_000 ones -> 9_999 tokens)
    chain = ["1"] + ["1", "+"] * 4_999
    assert len(chain) == 9_999
    assert function(chain) == 5_000

    # Right-heavy: pushes 5_000 operands before reducing (stack depth stress)
    right_heavy = ["1"] * 5_000 + ["+"] * 4_999
    assert len(right_heavy) == 9_999
    assert function(right_heavy) == 5_000


def _right_heavy(size):
    operands = size // 2 + 1
    return ["1"] * operands + ["+"] * (operands - 1)


def _time_evaluate(function, size, runs=3):
    tokens = _right_heavy(size)
    started = time.perf_counter()
    for _ in range(runs):
        function(tokens)
    return (time.perf_counter() - started) * 1_000 / runs


def run_benchmark():
    names = [function.__name__ for function in ALL_IMPLEMENTATIONS]
    print("\nBenchmark: Evaluate RPN - expression right-heavy")
    print(f"{'Tokens':>10} | " + " | ".join(f"{name + ' (ms)':>18}" for name in names))
    print("-" * (13 + 21 * len(names)))
    for size in (1_000, 5_000, 10_000):
        timings = [_time_evaluate(function, size) for function in ALL_IMPLEMENTATIONS]
        print(f"{len(_right_heavy(size)):>10,} | " + " | ".join(f"{t:>18.4f}" for t in timings))


if __name__ == "__main__":
    run_benchmark()
