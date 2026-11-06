# Valid Palindrome

difficulty: Easy

## Problem Statement

Given a string `s`, determine if it is a palindrome considering only
alphanumeric characters and ignoring case.

Example:
```
Input:  "A man, a plan, a canal: Panama"
Output: true

Input:  "race a car"
Output: false
```

## Intuition

Two pointers scanning inward from both ends, skipping non-alphanumeric
characters via direct ASCII range checks (no regex, no extra string
allocation), and comparing lowercased character codes.

## Complexity

See [complexity.md](./complexity.md).
