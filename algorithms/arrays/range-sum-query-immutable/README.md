# Range Sum Query Immutable

difficulty: Medium

## Problem Statement

Given an integer array `nums` that does not change, implement a structure that
answers many `sumRange(left, right)` queries â€” the sum of `nums[left..right]`
inclusive â€” efficiently.

Example:
```
nums = [-2, 0, 3, -5, 2, -1]
sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3
```

## Intuition

Precompute a prefix-sum array once: `prefix[i] = sum(nums[0..i-1])`. Any range
sum is then `prefix[right + 1] - prefix[left]`, answered in constant time
after an `O(n)` one-time build.

## Complexity

See [complexity.md](./complexity.md).
