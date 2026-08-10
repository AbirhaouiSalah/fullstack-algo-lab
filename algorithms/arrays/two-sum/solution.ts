export function twoSum(nums: number[], target: number): number[] {
  const seen = new Map<number, number>();

  for (let i = 0; i < nums.length; i++) {
    const current = nums[i];
    if (current === undefined) {
      continue;
    }

    const complement = target - current;
    const previousIndex = seen.get(complement);
    if (previousIndex !== undefined) {
      return [previousIndex, i];
    }
    seen.set(current, i);
  }

  throw new Error("No two sum solution exists");
}
