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
