def largest_rectangle_area(heights: list[int]) -> int:
    increasing_bars: list[tuple[int, int]] = []
    largest_area = 0

    for index, height in enumerate(heights):
        start = index
        while increasing_bars and increasing_bars[-1][1] > height:
            bar_index, bar_height = increasing_bars.pop()
            area = bar_height * (index - bar_index)
            largest_area = max(largest_area, area)
            start = bar_index
        increasing_bars.append((start, height))

    for bar_index, bar_height in increasing_bars:
        area = bar_height * (len(heights) - bar_index)
        largest_area = max(largest_area, area)

    return largest_area


def solve(heights: list[int]) -> int:
    return largest_rectangle_area(heights)


def solve_hint_1(heights: list[int]) -> int:
    """Hint 1: one-pass increasing stack with start indices."""
    increasing_bars: list[tuple[int, int]] = []
    largest_area = 0

    for index, height in enumerate(heights):
        start = index
        while increasing_bars and increasing_bars[-1][1] > height:
            bar_index, bar_height = increasing_bars.pop()
            area = bar_height * (index - bar_index)
            largest_area = max(largest_area, area)
            start = bar_index
        increasing_bars.append((start, height))

    for bar_index, bar_height in increasing_bars:
        area = bar_height * (len(heights) - bar_index)
        largest_area = max(largest_area, area)

    return largest_area


def solve_hint_2(heights: list[int]) -> int:
    """Hint 2: compute previous/next smaller bar boundaries in two passes."""
    n = len(heights)
    if n == 0:
        return 0

    left_boundary = [-1] * n
    stack: list[int] = []

    for index in range(n):
        while stack and heights[stack[-1]] >= heights[index]:
            stack.pop()
        left_boundary[index] = stack[-1] if stack else -1
        stack.append(index)

    right_boundary = [n] * n
    stack.clear()

    for index in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[index]:
            stack.pop()
        right_boundary[index] = stack[-1] if stack else n
        stack.append(index)

    largest_area = 0
    for index in range(n):
        width = right_boundary[index] - left_boundary[index] - 1
        area = heights[index] * width
        largest_area = max(largest_area, area)

    return largest_area


def solve_hint_3(heights: list[int]) -> int:
    """Hint 3: left/right boundaries computed with a monotonic stack in one direction each."""
    n = len(heights)
    if n == 0:
        return 0

    left_boundary = [0] * n
    stack: list[int] = []

    for index in range(n):
        while stack and heights[stack[-1]] >= heights[index]:
            stack.pop()
        left_boundary[index] = stack[-1] + 1 if stack else 0
        stack.append(index)

    right_boundary = [0] * n
    stack.clear()

    for index in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[index]:
            stack.pop()
        right_boundary[index] = stack[-1] - 1 if stack else n - 1
        stack.append(index)

    largest_area = 0
    for index in range(n):
        width = right_boundary[index] - left_boundary[index] + 1
        area = heights[index] * width
        largest_area = max(largest_area, area)

    return largest_area


def solve_hint_4(heights: list[int]) -> int:
    """Hint 4: single-pass monotonic stack of indices (strictly increasing heights)."""
    n = len(heights)
    largest_area = 0
    stack: list[int] = []

    for index in range(n + 1):
        current_height = heights[index] if index < n else 0
        while stack and heights[stack[-1]] > current_height:
            bar_index = stack.pop()
            bar_height = heights[bar_index]
            left = stack[-1] + 1 if stack else 0
            width = index - left
            largest_area = max(largest_area, bar_height * width)
        stack.append(index)

    return largest_area
