# Daily Temperatures

## Problem Statement

Given daily temperatures, return for each day how many days must pass until a
warmer temperature. Use zero when no future day is warmer.

Example: `[73, 74, 75, 71, 69, 72, 76, 73]` returns
`[1, 1, 4, 2, 1, 1, 0, 0]`.

## Approach

Maintain a stack of indices whose temperatures have not yet found a warmer
day. A warmer current day resolves all cooler days at the top of the stack.

## Complexity

See [complexity.md](./complexity.md).

## References

- [NeetCode: Daily Temperatures](https://neetcode.io/problems/daily-temperatures/question?list=neetcode150)
- [LeetCode: Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)