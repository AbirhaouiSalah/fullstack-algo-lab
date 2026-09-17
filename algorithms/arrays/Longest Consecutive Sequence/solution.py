def solve(nums: list[int]) -> int:
    if not nums:
        return 0

    values = set(nums)          # O(n) lookups
    best = 0

    for num in values:
        # Only start a run at its smallest element.
        if num - 1 in values:
            continue

        current = num
        length = 1
        while current + 1 in values:
            current += 1
            length += 1

        best = max(best, length)

    return best

def solve2(nums):
    if not nums:
        return 0

    values = set(nums)         # O(n) to build
    best = 0

    for num in values:
        # Skip anything that is not the start of a run
        if num - 1 in values:
            continue           # O(1) hash lookup

        # num is a start: count how long its run is
        current = num
        length = 1
        while current + 1 in values:   # O(1) per step
            current += 1
            length += 1

        best = max(best, length)

    return best