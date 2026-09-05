# Spiral Matrix

difficulty: Medium

## Problem Statement

Given an `m x n` matrix, return all elements of the matrix in spiral order
(clockwise, starting from the top-left corner).

Example:
```
Input:
[[1,2,3,4],
 [5,6,7,8],
 [9,10,11,12]]

Output: [1,2,3,4,8,12,11,10,9,5,6,7]
```

## Intuition

Maintain four shrinking boundaries â€” `top`, `bottom`, `left`, `right` â€” and
walk the top row, right column, bottom row, then left column in order,
advancing each boundary inward after it's consumed. Stop once the boundaries
cross.

## Complexity

See [complexity.md](./complexity.md).
