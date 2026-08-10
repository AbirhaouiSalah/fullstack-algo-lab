# Two Sum

## Problem Statement

Given an array of integers `nums` and an integer `target`, return the indices
of the two numbers that add up to `target`.

## Intuition

A brute-force nested loop checks every pair in O(n^2). Using a hash map to
store seen values lets each element be checked against its complement in a
single pass.

## Complexity

See [complexity.md](./complexity.md).
