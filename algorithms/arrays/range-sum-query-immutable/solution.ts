export const benchmarkInput: unknown[] = [[-2, 0, 3, -5, 2, -1]];

export class NumArray {
  private prefix: number[];

  constructor(nums: number[]) {
    this.prefix = new Array(nums.length + 1).fill(0);
    for (let i = 0; i < nums.length; i++) {
       this.prefix[i + 1] = this.prefix[i]! + nums[i]!;

     }
  }

  sumRange(left: number, right: number): number {
    return this.prefix[right + 1]! - this.prefix[left]!;
  }
}

/**
 * Convenience wrapper for benchmarking/testing a batch of queries at once.
 */
export function solve(nums: number[], queries: [number, number][]): number[] {
  const na = new NumArray(nums);
  return queries.map(([left, right]) => na.sumRange(left, right));
}
