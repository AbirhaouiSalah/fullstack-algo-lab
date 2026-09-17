export const benchmarkInput: unknown[] = [[1, 2, 3, 3]];

/**
 * Naive brute force: two explicit nested loops.
 * Time: O(n^2)  Space: O(1)
 */
export function solveNaive(nums: number[]): boolean {
  if (nums.length <= 1) return false;

  for (let i = 0; i < nums.length; i++) {
    for (let j = 0; j < nums.length; j++) {
      if (i === j) continue;
      if (nums[i] === nums[j]) return true;
    }
  }

  return false;
}

/**
 * Brute force, recursive: mutually recursive walk replacing the two loops.
 * Time: O(n^2)  Space: O(n) call stack
 */
function containsValueFrom(nums: number[], target: number, j: number): boolean {
  if (j >= nums.length) return false;
  if (nums[j] === target) return true;
  return containsValueFrom(nums, target, j + 1);
}

function hasDuplicateFrom(nums: number[], i: number): boolean {
  if (i >= nums.length) return false;
  const target = nums[i];
  if (target === undefined) return false; // unreachable given the guard above, but satisfies the type checker
  if (containsValueFrom(nums, target, i + 1)) return true;
  return hasDuplicateFrom(nums, i + 1);
}

export function solveRecursive(nums: number[]): boolean {
  if (nums.length <= 1) return false;
  return hasDuplicateFrom(nums, 0);
}

/**
 * Optimal: single pass with a hash set tracking values seen so far.
 * Time: O(n)  Space: O(n)
 */
export function solveHashSet(nums: number[]): boolean {
  const seen = new Set<number>();

  for (const num of nums) {
    if (seen.has(num)) return true;
    seen.add(num);
  }

  return false;
}

// Kept as `solve` for scaffold/benchmark.ts convention — defaults to the
// optimal implementation.
export function solve(nums: number[]): boolean {
  return solveHashSet(nums);
}