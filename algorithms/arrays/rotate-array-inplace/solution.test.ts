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
