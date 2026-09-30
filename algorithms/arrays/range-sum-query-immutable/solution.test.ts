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
