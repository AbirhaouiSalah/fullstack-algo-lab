# Complexity Analysis: Contains Duplicate

## Time Complexity

`O(n)` — a single pass; each `Set.has` / `Set.add` (or Python `in` / `.add`) is
average `O(1)`.

## Space Complexity

`O(n)` — the hash set can hold up to `n` elements in the worst case (all
values unique).


# Complexity Analysis: Contains Duplicate

## Implementations

| Version         | Time     | Space  | Notes                                       |
|------------------|----------|--------|----------------------------------------------|
| `solveNaive`     | O(n²)    | O(1)   | Two explicit nested loops                     |
| `solveRecursive` | O(n²)    | O(n)   | Same search, expressed as mutual recursion    |
| `solveHashSet`   | O(n)     | O(n)   | Single pass, hash set of values seen so far   |

`solve()` defaults to `solveHashSet`, the intended solution per the problem's
recommended complexity.

## Empirical validation

`solution.test.ts` includes a scaling-analysis suite that times each
implementation at `n` and `10n` and checks the growth ratio: ~10x confirms
O(n), while a ratio well above 15x confirms worse-than-linear (O(n²))
growth. `solution.bench.ts` (run via `vitest bench`) gives raw ops/sec
numbers for a visual side-by-side.