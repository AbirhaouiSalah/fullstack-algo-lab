# Min Stack

## Problem Statement

Design a stack supporting `push`, `pop`, `top`, and `get_min`, where retrieving
the smallest value takes constant time.

## Approach

Store each value together with the minimum value at that stack depth. Removing
an entry restores the previous minimum automatically.

## Complexity

See [complexity.md](./complexity.md).

## References

- [NeetCode: Min Stack](https://neetcode.io/problems/minimum-stack/question?list=neetcode150)
- [LeetCode: Min Stack](https://leetcode.com/problems/min-stack/)