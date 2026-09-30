import { describe, it, expect } from "vitest";
import { twoSum } from "./solution";
import { benchmarkAlgorithm } from "../../benchmark";

// Test suite for the "Two Sum" problem, covering correctness and performance benchmarks.

describe("Two Sum — Solution Correctness Suite", () => {
  it("should return indices for a standard input", () => {
    expect(twoSum([2, 7, 11, 15], 9)).toEqual([0, 1]);
  });

  it("should handle unsorted arrays", () => {
    expect(twoSum([3, 2, 4], 6)).toEqual([1, 2]);
  });

  it("should process duplicate values correctly", () => {
    expect(twoSum([3, 3], 6)).toEqual([0, 1]);
  });

  it("should work with negative numbers", () => {
    expect(twoSum([-1, -2, -3, -4, -5], -8)).toEqual([2, 4]);
  });

  it("should handle the first and last elements as the pair", () => {
    expect(twoSum([4, 5, 6], 10)).toEqual([0, 2]);
  });

  it("should return the correct indices for a large array", () => {
    const nums = Array.from({ length: 1000 }, (_, i) => i);
    const target = 998 + 999; // Valid pair: 998 + 999 = 1997
    expect(twoSum(nums, target)).toEqual([998, 999]);
  });
});

describe("Two Sum — Performance & Scalability Benchmark", () => {
  it("should maintain O(N) execution time scaling bounds", () => {
    const results = benchmarkAlgorithm<{
      nums: number[];
      target: number;
    }>(
      (input) => twoSum(input.nums, input.target),
      (size) => {
        const nums = Array.from({ length: size }, (_, i) => i);
        // Target is formed by the last two elements
        const target = (size - 2) + (size - 1);
        return { nums, target };
      },
      [1_000, 10_000, 100_000]
    );

    // Output empirical performance metrics to log
    console.table(results);

    // Verify 100,000 element execution completes under 50ms
    const largeScaleResult = results.find((r) => r.inputSize === 100_000);
    expect(largeScaleResult?.executionTimeMs).toBeLessThan(50);
  });
});