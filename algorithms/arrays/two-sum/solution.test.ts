import { describe, expect, it } from "vitest";
import { twoSum } from "./solution";

describe("twoSum", () => {
  it("returns indices of the two numbers that add up to target", () => {
    expect(twoSum([2, 7, 11, 15], 9)).toEqual([0, 1]);
  });

  it("handles negative numbers", () => {
    expect(twoSum([-3, 4, 3, 90], 0)).toEqual([0, 2]);
  });

  it("throws when no solution exists", () => {
    expect(() => twoSum([1, 2], 100)).toThrow();
  });
});
