# Valid Parentheses

## Problem Statement

Given a string containing only `()[]{}`, determine whether every opening
bracket is closed by the same type of bracket in the correct order.

Example: `"{[()]}"` is valid; `"([)]"` is not.

## Approach

Push opening brackets onto a stack. For each closing bracket, check that it
matches the most recent opening bracket. The string is valid only if the stack
is empty at the end.

## Complexity

See [complexity.md](./complexity.md).

## References

- [NeetCode: Valid Parentheses](https://neetcode.io/problems/validate-parentheses/question?list=neetcode150)
- [LeetCode: Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)