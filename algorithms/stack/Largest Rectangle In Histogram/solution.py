def largest_rectangle_area(heights: list[int]) -> int:
    increasing_bars: list[tuple[int, int]] = []
    largest_area = 0

    for index, height in enumerate([*heights, 0]):
        start = index
        while increasing_bars and increasing_bars[-1][1] > height:
            start, previous_height = increasing_bars.pop()
            largest_area = max(largest_area, previous_height * (index - start))
        increasing_bars.append((start, height))

    return largest_area


def solve(heights: list[int]) -> int:
    return largest_rectangle_area(heights)