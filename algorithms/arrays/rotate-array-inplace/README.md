# Rotate Array Inplace

difficulty: Easy

## Problem Statement

Given an integer array `nums`, rotate the array to the right by `k` steps,
where `k` can be any non-negative integer (including values greater than
`nums.length`). Do it **in-place** with `O(1)` extra space.

Example:
```
Input:  nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
```

## Intuition

Reversing the whole array, then reversing the first `k` elements and the
remaining `n - k` elements separately, produces the rotated array without any
extra storage. Three linear passes, no auxiliary array.

## Complexity

See [complexity.md](./complexity.md).
