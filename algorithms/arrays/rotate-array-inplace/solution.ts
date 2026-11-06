export const benchmarkInput: unknown[] = [[1, 2, 3, 4, 5, 6, 7], 3];

function reverseRange(nums: number[], start: number, end: number): void {
  while (start < end) {
    [nums[start]!, nums[end]!] = [nums[end]!, nums[start]!];
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
