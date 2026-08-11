/**
 * Finds the indices of two numbers in the array that add up to the target.
 * Uses a hash map for O(n) time complexity.
 *
 * @param nums - Array of integers.
 * @param target - Target sum.
 * @returns Indices of the two numbers as a tuple [i, j], where i < j.
 * @throws Error if no solution exists.
 */
export function twoSum(nums: number[], target: number): [number, number] {
  const numMap = new Map<number, number>();

  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    if (numMap.has(complement)) {
      return [numMap.get(complement)!, i];
    }
    numMap.set(nums[i], i);
  }

  throw new Error("No two sum solution exists");
}

/**
 * benchmarkInput is consumed by scripts/algorithms/benchmark.ts to invoke
 * the exported solution function repeatedly with a representative payload.
 */
export const benchmarkInput: Array<{ nums: number[]; target: number }> = [
  { nums: [2, 7, 11, 15], target: 9 },
  { nums: [3, 2, 4], target: 6 },
  { nums: [3, 3], target: 6 },
];