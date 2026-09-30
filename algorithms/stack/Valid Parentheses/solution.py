def is_valid_parentheses(value: str) -> bool:
    matching_openers = {")": "(", "]": "[", "}": "{"}
    openers = set(matching_openers.values())
    stack: list[str] = []

    for character in value:
        if character in openers:
            stack.append(character)
        elif not stack or stack.pop() != matching_openers.get(character):
            return False

    return not stack


def solve(value: str) -> bool:
    return is_valid_parentheses(value)