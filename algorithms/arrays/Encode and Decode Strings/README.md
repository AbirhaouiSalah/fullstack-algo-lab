# Encode and Decode Strings

difficulty: Medium

## Problem Statement

TODO

## Intuition

TODO

## Complexity

See [complexity.md](./complexity.md).


Here are the main ways to cut (extract part of) a string in JavaScript/TypeScript:

## `substring(start, end)`

Extracts characters between two indices (end is exclusive). Negative or out-of-range values get clamped to `0`/`length`, and if `start > end`, it swaps them automatically.

```javascript
const s = "5:Hello";
s.substring(0, 1);   // "5"
s.substring(2, 7);   // "Hello"
s.substring(2);      // "Hello" (no end = to the end of the string)
```

## `slice(start, end)`

Same idea as `substring`, but handles **negative indices** by counting from the end — and does *not* swap `start`/`end` if reversed (returns `""` instead).

```javascript
const s = "5:Hello";
s.slice(2, 7);    // "Hello"
s.slice(-5);      // "Hello" (last 5 characters)
s.slice(2, -0);   // "" — careful, -0 behaves like 0, not "end"
s.slice(2, -1);   // "Hell" (up to, but excluding, the last character)
```

## `substr(start, length)` — deprecated, avoid

Takes a **length** instead of an end index, which sounds convenient but this method is legacy/deprecated. Don't rely on it in new code.

```javascript
"5:Hello".substr(2, 5); // "Hello" — works, but avoid using substr
```

## `split(separator)` — cuts into an array, not a substring

Different tool: breaks the *whole string* into pieces wherever `separator` occurs. Useful when every occurrence of the separator is meaningful — **not** useful when only specific occurrences matter (as you saw with the `:` delimiter case, where content can itself contain `:`).

```javascript
"a,b,c".split(",");        // ["a", "b", "c"]
"5:Hello5:World".split(":"); // ["5", "Hello5", "World"] — wrong tool for length-prefixed parsing
```

## `charAt(index)` / bracket access — single character

```javascript
"Hello"[0];        // "H"
"Hello".charAt(0); // "H"
```

## For your decode use case specifically

`slice`/`substring` are functionally identical for non-negative indices, so either works. The pattern you want is:

```typescript
const colonIndex = s.indexOf(':', i);           // find where to cut
const lengthPart = s.substring(i, colonIndex);   // cut out the length prefix
const contentPart = s.substring(colonIndex + 1, colonIndex + 1 + length); // cut out the content
```

`indexOf` finds *where* to cut, `substring`/`slice` does the actual cutting. `split` cuts everywhere at once and can't be pointed at "just this one occurrence," which is why it doesn't fit your length-prefix decoder.