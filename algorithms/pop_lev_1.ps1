<#
.SYNOPSIS
    Scaffolds and populates the Level 1 (Tableaux & Chaînes de caractères) exercises:
    - arrays/rotate-array-inplace
    - arrays/range-sum-query-immutable
    - arrays/spiral-matrix
    - strings/reverse-string-inplace
    - strings/valid-palindrome
    - strings/caesar-cipher

.DESCRIPTION
    Calls the existing create-problem.ps1 for each problem (so folder creation,
    category handling, and README/complexity scaffolding stay consistent with the
    rest of the lab), then overwrites the placeholder solution/test/doc files with
    full implementations.

    Run this from the same directory as create-problem.ps1 (e.g. algorithms/scripts),
    or adjust $ScriptDir below.

.EXAMPLE
    .\populate-level1.ps1
#>

$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot
$CreateProblem = Join-Path $ScriptDir "create-problem.ps1"

if (-not (Test-Path $CreateProblem)) {
    Write-Error "create-problem.ps1 not found next to this script. Place populate-level1.ps1 in the same folder as create-problem.ps1, or edit `$CreateProblem`."
    exit 1
}

$repoRoot = Resolve-Path (Join-Path $ScriptDir "..")

function New-OrSkip-Problem {
    param(
        [string]$Category,
        [string]$Name,
        [string]$Difficulty
    )

    $problemPath = Join-Path $repoRoot "algorithms/$Category/$Name"
    if (Test-Path $problemPath) {
        Write-Host "Already exists, will overwrite content: $problemPath" -ForegroundColor Yellow
    } else {
        & $CreateProblem -Category $Category -Name $Name -Difficulty $Difficulty
    }
    return $problemPath
}

function Set-ProblemFiles {
    param(
        [string]$ProblemPath,
        [string]$Readme,
        [string]$SolutionTs,
        [string]$SolutionPy,
        [string]$TestTs,
        [string]$Complexity
    )

    Set-Content -Path (Join-Path $ProblemPath "README.md") -Value $Readme -Encoding UTF8
    Set-Content -Path (Join-Path $ProblemPath "solution.ts") -Value $SolutionTs -Encoding UTF8
    Set-Content -Path (Join-Path $ProblemPath "solution.py") -Value $SolutionPy -Encoding UTF8
    Set-Content -Path (Join-Path $ProblemPath "solution.test.ts") -Value $TestTs -Encoding UTF8
    Set-Content -Path (Join-Path $ProblemPath "complexity.md") -Value $Complexity -Encoding UTF8
}

# ============================================================
# 1. arrays/rotate-array-inplace (Easy)
# ============================================================
$p = New-OrSkip-Problem -Category "arrays" -Name "rotate-array-inplace" -Difficulty "Easy"

$readme = @'
# Rotate Array Inplace

difficulty: Easy

## Problem Statement

Given an integer array `nums`, rotate the array to the right by `k` steps,
where `k` can be any non-negative integer (including values greater than
`nums.length`). Do it **in-place** with `O(1)` extra space.

Example:
```
Input:  nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
```

## Intuition

Reversing the whole array, then reversing the first `k` elements and the
remaining `n - k` elements separately, produces the rotated array without any
extra storage. Three linear passes, no auxiliary array.

## Complexity

See [complexity.md](./complexity.md).
'@

$solutionTs = @'
export const benchmarkInput: unknown[] = [[1, 2, 3, 4, 5, 6, 7], 3];

function reverseRange(nums: number[], start: number, end: number): void {
  while (start < end) {
    [nums[start], nums[end]] = [nums[end], nums[start]];
    start++;
    end--;
  }
}

export function solve(nums: number[], k: number): void {
  const n = nums.length;
  if (n === 0) return;

  const shift = ((k % n) + n) % n;

  reverseRange(nums, 0, n - 1);
  reverseRange(nums, 0, shift - 1);
  reverseRange(nums, shift, n - 1);
}
'@

$solutionPy = @'
def solve(nums, k):
    n = len(nums)
    if n == 0:
        return

    k %= n

    def reverse(start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
'@

$testTs = @'
import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("rotate-array-inplace", () => {
  it("rotates by k less than length", () => {
    const nums = [1, 2, 3, 4, 5, 6, 7];
    solve(nums, 3);
    expect(nums).toEqual([5, 6, 7, 1, 2, 3, 4]);
  });

  it("handles k greater than array length", () => {
    const nums = [1, 2, 3];
    solve(nums, 4);
    expect(nums).toEqual([3, 1, 2]);
  });

  it("handles k = 0", () => {
    const nums = [1, 2, 3];
    solve(nums, 0);
    expect(nums).toEqual([1, 2, 3]);
  });

  it("handles a single-element array", () => {
    const nums = [42];
    solve(nums, 5);
    expect(nums).toEqual([42]);
  });

  it("handles an empty array without throwing", () => {
    const nums: number[] = [];
    expect(() => solve(nums, 3)).not.toThrow();
  });
});
'@

$complexity = @'
# Complexity Analysis: Rotate Array Inplace

## Time Complexity

`O(n)` — each element is touched a constant number of times across the three
reversal passes.

## Space Complexity

`O(1)` — rotation happens in place; no auxiliary array is allocated.
'@

Set-ProblemFiles -ProblemPath $p -Readme $readme -SolutionTs $solutionTs -SolutionPy $solutionPy -TestTs $testTs -Complexity $complexity

# ============================================================
# 2. arrays/range-sum-query-immutable (Medium)
# ============================================================
$p = New-OrSkip-Problem -Category "arrays" -Name "range-sum-query-immutable" -Difficulty "Medium"

$readme = @'
# Range Sum Query Immutable

difficulty: Medium

## Problem Statement

Given an integer array `nums` that does not change, implement a structure that
answers many `sumRange(left, right)` queries — the sum of `nums[left..right]`
inclusive — efficiently.

Example:
```
nums = [-2, 0, 3, -5, 2, -1]
sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3
```

## Intuition

Precompute a prefix-sum array once: `prefix[i] = sum(nums[0..i-1])`. Any range
sum is then `prefix[right + 1] - prefix[left]`, answered in constant time
after an `O(n)` one-time build.

## Complexity

See [complexity.md](./complexity.md).
'@

$solutionTs = @'
export const benchmarkInput: unknown[] = [[-2, 0, 3, -5, 2, -1]];

export class NumArray {
  private prefix: number[];

  constructor(nums: number[]) {
    this.prefix = new Array(nums.length + 1).fill(0);
    for (let i = 0; i < nums.length; i++) {
      this.prefix[i + 1] = this.prefix[i] + nums[i];
    }
  }

  sumRange(left: number, right: number): number {
    return this.prefix[right + 1] - this.prefix[left];
  }
}

/**
 * Convenience wrapper for benchmarking/testing a batch of queries at once.
 */
export function solve(nums: number[], queries: [number, number][]): number[] {
  const na = new NumArray(nums);
  return queries.map(([left, right]) => na.sumRange(left, right));
}
'@

$solutionPy = @'
class NumArray:
    def __init__(self, nums):
        self.prefix = [0] * (len(nums) + 1)
        for i, n in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + n

    def sum_range(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]


def solve(nums, queries):
    na = NumArray(nums)
    return [na.sum_range(left, right) for left, right in queries]
'@

$testTs = @'
import { describe, expect, it } from "vitest";
import { NumArray, solve } from "./solution";

describe("range-sum-query-immutable", () => {
  it("answers sumRange queries via the class", () => {
    const na = new NumArray([-2, 0, 3, -5, 2, -1]);
    expect(na.sumRange(0, 2)).toBe(1);
    expect(na.sumRange(2, 5)).toBe(-1);
    expect(na.sumRange(0, 5)).toBe(-3);
  });

  it("answers a batch of queries via solve()", () => {
    const result = solve(
      [1, 2, 3, 4, 5],
      [
        [0, 0],
        [1, 3],
        [0, 4],
      ],
    );
    expect(result).toEqual([1, 9, 15]);
  });

  it("handles a single-element range", () => {
    const na = new NumArray([7]);
    expect(na.sumRange(0, 0)).toBe(7);
  });
});
'@

$complexity = @'
# Complexity Analysis: Range Sum Query Immutable

## Time Complexity

- Build (constructor): `O(n)`
- Each `sumRange` query: `O(1)`

## Space Complexity

`O(n)` for the prefix-sum array.
'@

Set-ProblemFiles -ProblemPath $p -Readme $readme -SolutionTs $solutionTs -SolutionPy $solutionPy -TestTs $testTs -Complexity $complexity

# ============================================================
# 3. arrays/spiral-matrix (Medium)
# ============================================================
$p = New-OrSkip-Problem -Category "arrays" -Name "spiral-matrix" -Difficulty "Medium"

$readme = @'
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

Maintain four shrinking boundaries — `top`, `bottom`, `left`, `right` — and
walk the top row, right column, bottom row, then left column in order,
advancing each boundary inward after it's consumed. Stop once the boundaries
cross.

## Complexity

See [complexity.md](./complexity.md).
'@

$solutionTs = @'
export const benchmarkInput: unknown[] = [
  [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
  ],
];

export function solve(matrix: number[][]): number[] {
  if (matrix.length === 0 || matrix[0].length === 0) return [];

  const result: number[] = [];
  let top = 0;
  let bottom = matrix.length - 1;
  let left = 0;
  let right = matrix[0].length - 1;

  while (top <= bottom && left <= right) {
    for (let col = left; col <= right; col++) result.push(matrix[top][col]);
    top++;

    for (let row = top; row <= bottom; row++) result.push(matrix[row][right]);
    right--;

    if (top <= bottom) {
      for (let col = right; col >= left; col--) result.push(matrix[bottom][col]);
      bottom--;
    }

    if (left <= right) {
      for (let row = bottom; row >= top; row--) result.push(matrix[row][left]);
      left++;
    }
  }

  return result;
}
'@

$solutionPy = @'
def solve(matrix):
    if not matrix or not matrix[0]:
        return []

    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result
'@

$testTs = @'
import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("spiral-matrix", () => {
  it("walks a rectangular matrix in spiral order", () => {
    const matrix = [
      [1, 2, 3, 4],
      [5, 6, 7, 8],
      [9, 10, 11, 12],
    ];
    expect(solve(matrix)).toEqual([1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]);
  });

  it("walks a square matrix in spiral order", () => {
    const matrix = [
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9],
    ];
    expect(solve(matrix)).toEqual([1, 2, 3, 6, 9, 8, 7, 4, 5]);
  });

  it("handles a single row", () => {
    expect(solve([[1, 2, 3]])).toEqual([1, 2, 3]);
  });

  it("handles a single column", () => {
    expect(solve([[1], [2], [3]])).toEqual([1, 2, 3]);
  });

  it("handles an empty matrix", () => {
    expect(solve([])).toEqual([]);
  });
});
'@

$complexity = @'
# Complexity Analysis: Spiral Matrix

## Time Complexity

`O(m * n)` — every cell is visited exactly once.

## Space Complexity

`O(1)` extra space, excluding the output array (which necessarily holds
`m * n` elements).
'@

Set-ProblemFiles -ProblemPath $p -Readme $readme -SolutionTs $solutionTs -SolutionPy $solutionPy -TestTs $testTs -Complexity $complexity

# ============================================================
# 4. strings/reverse-string-inplace (Easy)
# ============================================================
$p = New-OrSkip-Problem -Category "strings" -Name "reverse-string-inplace" -Difficulty "Easy"

$readme = @'
# Reverse String Inplace

difficulty: Easy

## Problem Statement

Given an array of characters `chars`, reverse it **in-place** with `O(1)`
extra space.

Example:
```
Input:  ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]
```

## Intuition

Two pointers starting at each end, swapping and moving inward until they
meet, cross, or coincide.

## Complexity

See [complexity.md](./complexity.md).
'@

$solutionTs = @'
export const benchmarkInput: unknown[] = [["h", "e", "l", "l", "o"]];

export function solve(chars: string[]): void {
  let left = 0;
  let right = chars.length - 1;

  while (left < right) {
    [chars[left], chars[right]] = [chars[right], chars[left]];
    left++;
    right--;
  }
}
'@

$solutionPy = @'
def solve(chars):
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
'@

$testTs = @'
import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("reverse-string-inplace", () => {
  it("reverses an even-length array", () => {
    const chars = ["h", "e", "l", "l", "o", "!"];
    solve(chars);
    expect(chars).toEqual(["!", "o", "l", "l", "e", "h"]);
  });

  it("reverses an odd-length array", () => {
    const chars = ["h", "e", "l", "l", "o"];
    solve(chars);
    expect(chars).toEqual(["o", "l", "l", "e", "h"]);
  });

  it("leaves a single-character array unchanged", () => {
    const chars = ["x"];
    solve(chars);
    expect(chars).toEqual(["x"]);
  });

  it("handles an empty array without throwing", () => {
    const chars: string[] = [];
    expect(() => solve(chars)).not.toThrow();
  });
});
'@

$complexity = @'
# Complexity Analysis: Reverse String Inplace

## Time Complexity

`O(n)` — one pass, `n / 2` swaps.

## Space Complexity

`O(1)` — swaps happen in place.
'@

Set-ProblemFiles -ProblemPath $p -Readme $readme -SolutionTs $solutionTs -SolutionPy $solutionPy -TestTs $testTs -Complexity $complexity

# ============================================================
# 5. strings/valid-palindrome (Easy)
# ============================================================
$p = New-OrSkip-Problem -Category "strings" -Name "valid-palindrome" -Difficulty "Easy"

$readme = @'
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
'@

$solutionTs = @'
export const benchmarkInput: unknown[] = ["A man, a plan, a canal: Panama"];

function isAlphanumeric(code: number): boolean {
  return (
    (code >= 48 && code <= 57) || // 0-9
    (code >= 65 && code <= 90) || // A-Z
    (code >= 97 && code <= 122) // a-z
  );
}

function toLowerCode(code: number): number {
  return code >= 65 && code <= 90 ? code + 32 : code;
}

export function solve(s: string): boolean {
  let left = 0;
  let right = s.length - 1;

  while (left < right) {
    const leftCode = s.charCodeAt(left);
    const rightCode = s.charCodeAt(right);

    if (!isAlphanumeric(leftCode)) {
      left++;
      continue;
    }
    if (!isAlphanumeric(rightCode)) {
      right--;
      continue;
    }
    if (toLowerCode(leftCode) !== toLowerCode(rightCode)) return false;

    left++;
    right--;
  }

  return true;
}
'@

$solutionPy = @'
def solve(s):
    left, right = 0, len(s) - 1

    while left < right:
        if not s[left].isalnum():
            left += 1
            continue
        if not s[right].isalnum():
            right -= 1
            continue
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1

    return True
'@

$testTs = @'
import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("valid-palindrome", () => {
  it("returns true for a palindrome with punctuation and mixed case", () => {
    expect(solve("A man, a plan, a canal: Panama")).toBe(true);
  });

  it("returns false for a non-palindrome", () => {
    expect(solve("race a car")).toBe(false);
  });

  it("returns true for an empty string", () => {
    expect(solve("")).toBe(true);
  });

  it("returns true for a single character", () => {
    expect(solve("a")).toBe(true);
  });

  it("returns true when the string has no alphanumeric characters", () => {
    expect(solve(".,!?")).toBe(true);
  });

  it("returns true for numeric palindromes", () => {
    expect(solve("12321")).toBe(true);
  });
});
'@

$complexity = @'
# Complexity Analysis: Valid Palindrome

## Time Complexity

`O(n)` — each character is visited at most once across the two pointers.

## Space Complexity

`O(1)` — no auxiliary string or array is built; comparisons happen directly
on character codes.
'@

Set-ProblemFiles -ProblemPath $p -Readme $readme -SolutionTs $solutionTs -SolutionPy $solutionPy -TestTs $testTs -Complexity $complexity

# ============================================================
# 6. strings/caesar-cipher (Easy)
# ============================================================
$p = New-OrSkip-Problem -Category "strings" -Name "caesar-cipher" -Difficulty "Easy"

$readme = @'
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
'@

$solutionTs = @'
export const benchmarkInput: unknown[] = ["Hello, World!", 3];

const UPPER_A = "A".charCodeAt(0);
const UPPER_Z = "Z".charCodeAt(0);
const LOWER_A = "a".charCodeAt(0);
const LOWER_Z = "z".charCodeAt(0);

export function solve(text: string, shift: number): string {
  const normalizedShift = ((shift % 26) + 26) % 26;
  let result = "";

  for (let i = 0; i < text.length; i++) {
    const code = text.charCodeAt(i);

    if (code >= UPPER_A && code <= UPPER_Z) {
      result += String.fromCharCode(((code - UPPER_A + normalizedShift) % 26) + UPPER_A);
    } else if (code >= LOWER_A && code <= LOWER_Z) {
      result += String.fromCharCode(((code - LOWER_A + normalizedShift) % 26) + LOWER_A);
    } else {
      result += text[i];
    }
  }

  return result;
}
'@

$solutionPy = @'
def solve(text, shift):
    normalized_shift = shift % 26
    result = []

    for ch in text:
        if "A" <= ch <= "Z":
            result.append(chr((ord(ch) - ord("A") + normalized_shift) % 26 + ord("A")))
        elif "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") + normalized_shift) % 26 + ord("a")))
        else:
            result.append(ch)

    return "".join(result)
'@

$testTs = @'
import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("caesar-cipher", () => {
  it("shifts letters and preserves punctuation/case", () => {
    expect(solve("Hello, World!", 3)).toBe("Khoor, Zruog!");
  });

  it("wraps around the end of the alphabet", () => {
    expect(solve("xyz", 3)).toBe("abc");
  });

  it("handles a shift of 0", () => {
    expect(solve("Hello", 0)).toBe("Hello");
  });

  it("handles a shift larger than 26", () => {
    expect(solve("abc", 29)).toBe("def");
  });

  it("handles a negative shift", () => {
    expect(solve("abc", -1)).toBe("zab");
  });

  it("leaves digits and spaces untouched", () => {
    expect(solve("Room 42, now!", 1)).toBe("Sppn 42, opx!");
  });
});
'@

$complexity = @'
# Complexity Analysis: Caesar Cipher

## Time Complexity

`O(n)` — one pass over the input string.

## Space Complexity

`O(n)` — the output string is the same length as the input.
'@

Set-ProblemFiles -ProblemPath $p -Readme $readme -SolutionTs $solutionTs -SolutionPy $solutionPy -TestTs $testTs -Complexity $complexity

Write-Host ""
Write-Host "Level 1 scaffolding complete:" -ForegroundColor Green
Write-Host "  arrays/rotate-array-inplace"
Write-Host "  arrays/range-sum-query-immutable"
Write-Host "  arrays/spiral-matrix"
Write-Host "  strings/reverse-string-inplace"
Write-Host "  strings/valid-palindrome"
Write-Host "  strings/caesar-cipher"
Write-Host ""
Write-Host "Run '.\test-all.ps1' to execute Vitest across all problems and refresh the progress report." -ForegroundColor Cyan