"""
Climbing Stairs — all standard solutions.

Problem
-------
You can climb 1 or 2 steps at a time. Given n, return the number of distinct
ways to reach the top.

Recurrence
----------
ways(n) = ways(n - 1) + ways(n - 2)
ways(1) = 1
ways(2) = 2

This is Fibonacci shifted by one index.
"""

from functools import lru_cache


# ---------------------------------------------------------------------------
# 1. Naive recursion — O(2^n) time, O(n) space (call stack)
# ---------------------------------------------------------------------------
def solve_recursive(n: int) -> int:
    if n <= 2:
        return n
    return solve_recursive(n - 1) + solve_recursive(n - 2)


# ---------------------------------------------------------------------------
# 2. Memoized recursion (top-down DP) — O(n) time, O(n) space
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def _memo(n: int) -> int:
    if n <= 2:
        return n
    return _memo(n - 1) + _memo(n - 2)


def solve_memo(n: int) -> int:
    return _memo(n)


# ---------------------------------------------------------------------------
# 3. Bottom-up DP with an array — O(n) time, O(n) space
# ---------------------------------------------------------------------------
def solve_dp_array(n: int) -> int:
    if n <= 2:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2

    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


# ---------------------------------------------------------------------------
# 4. Bottom-up DP with O(1) space (two rolling variables)
#    This is the recommended solution.
# ---------------------------------------------------------------------------
def solve_dp_constant(n: int) -> int:
    if n <= 2:
        return n

    prev, curr = 1, 2  # ways(1), ways(2)
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr


# ---------------------------------------------------------------------------
# 5. Matrix exponentiation — O(log n) time, O(1) space
#    Uses [[1,1],[1,0]]^n to compute Fibonacci in logarithmic time.
#    Overkill for n <= 45, but included for completeness.
# ---------------------------------------------------------------------------
def _mat_mul(a, b):
    return (
        a[0] * b[0] + a[1] * b[2],
        a[0] * b[1] + a[1] * b[3],
        a[2] * b[0] + a[3] * b[2],
        a[2] * b[1] + a[3] * b[3],
    )


def _mat_pow(m, p):
    result = (1, 0, 0, 1)  # identity matrix
    while p > 0:
        if p & 1:
            result = _mat_mul(result, m)
        m = _mat_mul(m, m)
        p >>= 1
    return result


def solve_matrix(n: int) -> int:
    if n <= 2:
        return n
    # ways(n) = F(n+1) where F(1)=1, F(2)=1, F(3)=2, ...
    # With M = [[1,1],[1,0]], M^k = [[F(k+1), F(k)], [F(k), F(k-1)]]
    m = _mat_pow((1, 1, 1, 0), n)
    return m[0]  # F(n+1)


# ---------------------------------------------------------------------------
# 6. Closed form (Binet's formula) — O(1) time, O(1) space
#    Floating-point; safe for n <= 45 but not for very large n.
# ---------------------------------------------------------------------------
def solve_binet(n: int) -> int:
    if n <= 2:
        return n
    sqrt5 = 5 ** 0.5
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    # ways(n) = F(n+1) = (phi^(n+1) - psi^(n+1)) / sqrt5
    return round((phi ** (n + 1) - psi ** (n + 1)) / sqrt5)


# ---------------------------------------------------------------------------
# Default entrypoint used by the test runner.
# ---------------------------------------------------------------------------
def solve(n: int) -> int:
    """Return the number of distinct ways to climb n stairs (1 or 2 steps)."""
    return solve_dp_constant(n)


# ---------------------------------------------------------------------------
# Self-check: all approaches must agree for n = 1 .. 45
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    implementations = {
        "recursive": solve_recursive,
        "memo": solve_memo,
        "dp_array": solve_dp_array,
        "dp_constant": solve_dp_constant,
        "matrix": solve_matrix,
        "binet": solve_binet,
    }

    reference = [solve_dp_constant(n) for n in range(1, 46)]

    for name, fn in implementations.items():
        results = [fn(n) for n in range(1, 46)]
        status = "OK" if results == reference else "MISMATCH"
        print(f"{name:>12}: {status}")

    print("\nways(1..10) =", reference[:10])
    print("ways(45)    =", reference[-1])