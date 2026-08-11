import { describe, expect, it } from "vitest";
import { solve, solveNaive, solveRecursive, solveHashSet } from "./solution";

const implementations: Array<{ name: string; fn: (nums: number[]) => boolean }> = [
  { name: "solveNaive", fn: solveNaive },
  { name: "solveRecursive", fn: solveRecursive },
  { name: "solveHashSet", fn: solveHashSet },
];

describe.each(implementations)("contains-duplicate - $name", ({ fn }) => {
  it("returns true when a value repeats", () => {
    expect(fn([1, 2, 3, 3])).toBe(true);
  });

  it("returns false when all values are unique", () => {
    expect(fn([1, 2, 3, 4])).toBe(false);
  });

  it("returns false for an empty array", () => {
    expect(fn([])).toBe(false);
  });

  it("returns false for a single-element array", () => {
    expect(fn([5])).toBe(false);
  });

  it("handles negative numbers", () => {
    expect(fn([-1, -2, -1])).toBe(true);
  });

  it("handles large value ranges near the constraint bounds", () => {
    expect(fn([1000000000, -1000000000, 1000000000])).toBe(true);
  });
});

describe("contains-duplicate - default export", () => {
  it("solve() delegates to the hash-set implementation", () => {
    expect(solve([1, 2, 3, 3])).toBe(true);
    expect(solve([1, 2, 3, 4])).toBe(false);
  });
});

function generateUniqueArray(size: number): number[] {
  return Array.from({ length: size }, (_, i) => i);
}

function timeFn(fn: (nums: number[]) => boolean, size: number): number {
  const arr = generateUniqueArray(size);
  const start = performance.now();
  fn(arr);
  return performance.now() - start;
}

function avgTime(fn: (nums: number[]) => boolean, size: number, runs = 5): number {
  let total = 0;
  for (let i = 0; i < runs; i++) total += timeFn(fn, size);
  return total / runs;
}

// Runs under `vitest run` (test-all.ps1). Empirically checks that each
// implementation's growth rate matches its expected Big O as input size
// scales up 10x. Worst-case input (no duplicates) forces the full search
// in every implementation.
describe("contains-duplicate scaling analysis", () => {
  it("solveHashSet scales roughly linearly (O(n))", () => {
    avgTime(solveHashSet, 1_000); // JIT warm-up

    const small = 5_000;
    const large = 50_000; // 10x
    const smallTime = avgTime(solveHashSet, small);
    const largeTime = avgTime(solveHashSet, large);
    const ratio = largeTime / smallTime;

    console.log(
      `[perf] solveHashSet    n=${small}: ${smallTime.toFixed(3)}ms | n=${large}: ${largeTime.toFixed(3)}ms | ratio: ${ratio.toFixed(2)}x`,
    );

    // O(n) -> ~10x growth, O(n^2) -> ~100x. 30x leaves headroom for noise.
    expect(ratio).toBeLessThan(30);
  });

  it("solveNaive scales roughly quadratically (O(n^2))", () => {
    avgTime(solveNaive, 200);

    const small = 400;
    const large = 4_000; // 10x
    const smallTime = avgTime(solveNaive, small, 3);
    const largeTime = avgTime(solveNaive, large, 3);
    const ratio = largeTime / smallTime;

    console.log(
      `[perf] solveNaive      n=${small}: ${smallTime.toFixed(3)}ms | n=${large}: ${largeTime.toFixed(3)}ms | ratio: ${ratio.toFixed(2)}x`,
    );

    expect(ratio).toBeGreaterThan(15);
  });

  it("solveRecursive scales roughly quadratically (O(n^2))", () => {
    // Kept small on purpose: recursion depth grows with n and this is not
    // tail-call optimized in V8, so large n risks a stack overflow.
    avgTime(solveRecursive, 200);

    const small = 300;
    const large = 3_000; // 10x
    const smallTime = avgTime(solveRecursive, small, 3);
    const largeTime = avgTime(solveRecursive, large, 3);
    const ratio = largeTime / smallTime;

    console.log(
      `[perf] solveRecursive  n=${small}: ${smallTime.toFixed(3)}ms | n=${large}: ${largeTime.toFixed(3)}ms | ratio: ${ratio.toFixed(2)}x`,
    );

    expect(ratio).toBeGreaterThan(15);
  });
});