OPERATORS = frozenset("+-*/")


def _truncating_divide(left: int, right: int) -> int:
    """Integer division truncating toward zero, using exact integer math.

    Python's // floors (-7 // 2 == -4) and int(left / right) goes through floats,
    which loses precision on big intermediates. This does neither.
    """
    quotient = abs(left) // abs(right)
    return quotient if (left < 0) == (right < 0) else -quotient


def eval_rpn(tokens: list[str]) -> int:
    """Optimal solution: stack + operator table. O(n) time, O(n) space."""
    operations = {
        "+": lambda left, right: left + right,
        "-": lambda left, right: left - right,
        "*": lambda left, right: left * right,
        "/": _truncating_divide,
    }
    stack: list[int] = []

    for token in tokens:
        if token in operations:
            right = stack.pop()
            left = stack.pop()
            stack.append(operations[token](left, right))
        else:
            stack.append(int(token))

    return stack[-1]


def solve(tokens: list[str]) -> int:
    return eval_rpn(tokens)


def solve_hint_1(tokens: list[str]) -> int:
    """Hint 1 (brute force): repeatedly find the first operator and replace it,
    with the two operands to its left, by their result.

    Each replacement is O(n) (search + list surgery) and there are up to n/2 of
    them -> O(n^2) time.
    """
    expression = list(tokens)

    while len(expression) > 1:
        index = next(i for i, token in enumerate(expression) if token in OPERATORS)
        left = int(expression[index - 2])
        right = int(expression[index - 1])
        operator = expression[index]

        if operator == "+":
            result = left + right
        elif operator == "-":
            result = left - right
        elif operator == "*":
            result = left * right
        else:
            result = _truncating_divide(left, right)

        expression[index - 2 : index + 1] = [str(result)]

    return int(expression[0])


def solve_hint_2(tokens: list[str]) -> int:
    """Hint 2: stack with explicit operator branches.

    A number is pushed. An operator pops two operands (the right one comes off
    first!), computes, and pushes the result back. O(n) time, O(n) space.
    """
    stack: list[int] = []

    for token in tokens:
        if token == "+":
            right = stack.pop()
            left = stack.pop()
            stack.append(left + right)
        elif token == "-":
            right = stack.pop()
            left = stack.pop()
            stack.append(left - right)
        elif token == "*":
            right = stack.pop()
            left = stack.pop()
            stack.append(left * right)
        elif token == "/":
            right = stack.pop()
            left = stack.pop()
            stack.append(_truncating_divide(left, right))
        else:
            stack.append(int(token))

    return stack.pop()


def solve_hint_3(tokens: list[str]) -> int:
    """Hint 3: the stack always exposes the most recent operands (the ones
    closest to the operator); once every token is consumed the final result is
    the only value left in the stack.
    """
    stack: list[int] = []

    for token in tokens:
        if token in OPERATORS:
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(_truncating_divide(left, right))
        else:
            stack.append(int(token))

    assert len(stack) == 1, "a valid RPN expression leaves exactly one value"
    return stack[0]