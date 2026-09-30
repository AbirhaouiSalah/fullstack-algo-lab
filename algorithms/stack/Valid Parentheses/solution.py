def is_valid_parentheses(value: str) -> bool:
    """Optimal solution: stack + closing-to-opening map. O(n) time, O(n) space."""
    matching_openers = {")": "(", "]": "[", "}": "{"}
    openers = set(matching_openers.values())
    stack: list[str] = []

    for character in value:
        if character in openers:
            stack.append(character)
        elif not stack or stack.pop() != matching_openers[character]:
            return False

    return not stack


def solve(value: str) -> bool:
    return is_valid_parentheses(value)


def solve_hint_1(value: str) -> bool:
    """Hint 1 (brute force): keep removing adjacent valid pairs until stuck.

    Each pass is O(n) and there can be up to n/2 passes -> O(n^2) time.
    If the string ends up empty, every bracket was matched.
    """
    previous = None
    while previous != value:
        previous = value
        value = value.replace("()", "").replace("[]", "").replace("{}", "")
    return value == ""


def solve_hint_2(value: str) -> bool:
    """Hint 2: stack with explicit bracket matching branches.

    Push every opener. On a closer, the top of the stack must be the matching
    opener, otherwise return False immediately. O(n) time, O(n) space.
    """
    stack: list[str] = []

    for character in value:
        if character == "(" or character == "[" or character == "{":
            stack.append(character)
        elif character == ")":
            if not stack or stack[-1] != "(":
                return False
            stack.pop()
        elif character == "]":
            if not stack or stack[-1] != "[":
                return False
            stack.pop()
        elif character == "}":
            if not stack or stack[-1] != "{":
                return False
            stack.pop()

    return len(stack) == 0


def solve_hint_3(value: str) -> bool:
    """Hint 3: the stack must be empty once the whole string is processed.

    A leftover opener means it never found its closer. Adds a cheap early exit:
    an odd length can never be balanced.
    """
    if len(value) % 2 == 1:
        return False

    matching_openers = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for character in value:
        if character in matching_openers:
            if not stack or stack.pop() != matching_openers[character]:
                return False
        else:
            stack.append(character)

    return not stack