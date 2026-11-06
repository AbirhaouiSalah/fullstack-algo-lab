def solve(text, shift):
    normalized_shift = shift % 26
    result = []

    for ch in text:
        if "A" <= ch <= "Z":
            result.append(chr((ord(ch) - ord("A") + normalized_shift) % 26 + ord("A")))
        elif "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") + normalized_shift) % 26 + ord("a")))
        else:
            result.append(ch)

    return "".join(result)
