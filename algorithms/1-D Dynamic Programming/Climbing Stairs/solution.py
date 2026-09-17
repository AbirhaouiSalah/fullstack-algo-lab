def solve(n: int) -> int:
    """Return the number of distinct ways to climb n stairs (1 or 2 steps at a time)."""
    if n <= 2:
        return n

    prev, curr = 1, 2  # ways(1) = 1, ways(2) = 2
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr