def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    operators = {"+", "-", "*", "/"}

    for token in tokens:
        if token not in operators:
            stack.append(int(token))
            continue

        right = stack.pop()
        left = stack.pop()
        if token == "+":
            result = left + right
        elif token == "-":
            result = left - right
        elif token == "*":
            result = left * right
        else:
            quotient = abs(left) // abs(right)
            result = -quotient if (left < 0) != (right < 0) else quotient
        stack.append(result)

    return stack[-1]


def solve(tokens: list[str]) -> int:
    return eval_rpn(tokens)