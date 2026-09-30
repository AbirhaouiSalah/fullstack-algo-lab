def daily_temperatures(temperatures: list[int]) -> list[int]:
    """Optimal solution: monotonic (decreasing) stack of indices.

    Each index is pushed once and popped at most once -> O(n) time, O(n) space.
    """
    result = [0] * len(temperatures)
    stack: list[int] = []  # indices whose next warmer day is still unknown

    for index, temperature in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temperature:
            previous_index = stack.pop()
            result[previous_index] = index - previous_index
        stack.append(index)

    return result


def solve(temperatures: list[int]) -> list[int]:
    return daily_temperatures(temperatures)


def solve_hint_1(temperatures: list[int]) -> list[int]:
    """Hint 1 (brute force): for each day, scan forward until a warmer day.

    O(n^2) time in the worst case (e.g. a non-increasing sequence), O(1) extra
    space besides the output.
    """
    size = len(temperatures)
    result = [0] * size

    for day in range(size):
        for next_day in range(day + 1, size):
            if temperatures[next_day] > temperatures[day]:
                result[day] = next_day - day
                break

    return result


def solve_hint_2(temperatures: list[int]) -> list[int]:
    """Hint 2 (reverse approach): standing on a day, resolve the earlier days.

    Earlier days wait on a stack as (temperature, index) pairs. When the current
    day is warmer than the waiting ones, it is their answer: pop them all.
    O(n) time, O(n) space.
    """
    result = [0] * len(temperatures)
    waiting: list[tuple[int, int]] = []  # (temperature, index)

    for index, temperature in enumerate(temperatures):
        while waiting and waiting[-1][0] < temperature:
            _, waiting_index = waiting.pop()
            result[waiting_index] = index - waiting_index
        waiting.append((temperature, index))

    return result


def solve_hint_3(temperatures: list[int]) -> list[int]:
    """Hint 3: stack of indices kept in monotonically decreasing temperature.

    Popping every index whose temperature is smaller than the current one keeps
    the stack decreasing, and the answer is the difference between indices.
    Indices still on the stack at the end never found a warmer day (answer 0).
    """
    result = [0] * len(temperatures)
    stack: list[int] = []

    for current in range(len(temperatures)):
        while stack and temperatures[current] > temperatures[stack[-1]]:
            top = stack.pop()
            result[top] = current - top
        stack.append(current)

    return result


def solve_bonus_jump_pointers(temperatures: list[int]) -> list[int]:
    """Bonus (follow-up): O(1) extra space, no stack.

    Walk right to left and reuse the answers already computed: if the day at
    `candidate` is not warmer, jump straight to the next warmer day of that
    candidate instead of stepping one by one. Amortized O(n) time.
    """
    size = len(temperatures)
    result = [0] * size

    for day in range(size - 2, -1, -1):
        candidate = day + 1
        while candidate < size and temperatures[candidate] <= temperatures[day]:
            if result[candidate] == 0:
                candidate = size  # nothing warmer to the right of candidate
                break
            candidate += result[candidate]

        if candidate < size:
            result[day] = candidate - day

    return result