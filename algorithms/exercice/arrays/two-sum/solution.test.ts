import { describe, it, expect } from "vitest";
import { twoSum } from "./solution";
import { benchmarkAlgorithm } from "../../../scripts/algorithms/benchmark";

describe("Two Sum — Solution Correctness Suite", () => {
  it("should solve standard array inputs", () => {
    expect(twoSum([2, 7, 11, 15], 9)).toEqual([0, 1]);
  });

  it("should handle un-sorted array inputs", () => {
    expect(twoSum([3, 2, 4], 6)).toEqual([1, 2]);
  });

  it("should process duplicate values correctly", () => {
    expect(twoSum([3, 3], 6)).toEqual([0, 1]);
  });
});

describe("Two Sum — Performance & Scalability Benchmark", () => {
  it("should maintain O(N) execution time scaling bounds", () => {
    const results = benchmarkAlgorithm(
      (input) => twoSum(input.nums, input.target),
      (size) => {
        const nums = Array.from({ length: size }, (_, i) => i);
        // Target is formed by last two elements
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