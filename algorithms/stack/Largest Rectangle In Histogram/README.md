# Largest Rectangle in Histogram

## Problem Statement

Given non-negative bar heights in a histogram, return the area of the largest
rectangle that can be formed using consecutive bars.

Example: `[2, 1, 5, 6, 2, 3]` has maximum rectangle area `10`.

## Approach

Keep bars in increasing height order with their earliest possible start index.
When a shorter bar arrives, pop taller bars and compute the largest rectangle
for each popped height.

## Complexity

See [complexity.md](./complexity.md).

## References

- [NeetCode: Largest Rectangle in Histogram](https://neetcode.io/problems/largest-rectangle-in-histogram/question?list=neetcode150)
- [LeetCode: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)