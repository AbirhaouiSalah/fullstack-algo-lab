# Caesar Cipher

difficulty: Easy

## Problem Statement

Given a string `text` and an integer `shift`, shift every letter by `shift`
positions in the alphabet, wrapping around as needed, preserving case and
leaving non-letter characters untouched.

Example:
```
Input:  text = "Hello, World!", shift = 3
Output: "Khoor, Zruog!"
```

## Intuition

Work directly on ASCII codes: detect the letter's case-range (`A-Z` or
`a-z`), normalize the shift into `[0, 26)`, and remap the code within that
26-letter range using modular arithmetic. Everything outside those ranges
(spaces, punctuation, digits) passes through unchanged.

## Complexity

See [complexity.md](./complexity.md).
