# Evaluate Reverse Polish Notation

## Problem Statement

Evaluate an arithmetic expression written in Reverse Polish Notation. The
supported operators are `+`, `-`, `*`, and `/`; division truncates toward
zero.

Example: `["2", "1", "+", "3", "*"]` evaluates to `9`.

## Approach

Push operands onto a stack. When an operator appears, pop the right and left
operands in that order, evaluate the operation, and push its result.

## Complexity

See [complexity.md](./complexity.md).

## References

- [NeetCode: Evaluate Reverse Polish Notation](https://neetcode.io/problems/evaluate-reverse-polish-notation/question?list=neetcode150)
- [LeetCode: Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)