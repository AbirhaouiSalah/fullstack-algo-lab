import { describe, it, expect } from "vitest";
import {
  isAnagram,
  isAnagramSort,
  isAnagramTwoMaps,
  algorithms,
  type AnagramFn,
} from "./solution";

// Test suite for the "Valid Anagram" problem, covering multiple implementations and performance benchmarks.

/* ================================================================== */
/*  Correctness tests – every algorithm must produce the same result  */
/* ================================================================== */

const correctnessCases: [string, string, boolean][] = [
  ["racecar", "carrace", true],
  ["jar", "jam", false],
  ["hello", "hello", true],
  ["a", "ab", false],
  ["", "", true],
  ["a", "a", true],
  ["a", "b", false],
  ["anagram", "nagaram", true],
  ["aab", "abb", false],
  ["listen", "silent", true],
  ["triangle", "integral", true],
  ["abc", "cba", true],
  ["abc", "abd", false],
];

describe.each(algorithms)("$name – correctness", ({ fn }) => {
  it.each(correctnessCases)(
    "isAnagram(%s, %s) → %s",
    (s, t, expected) => {
      expect(fn(s, t)).toBe(expected);
    }
  );
});

/* ================================================================== */
/*  Performance analysis                                               */
/* ================================================================== */

/**
 * Generate a random lowercase string of given length.
 */
function randomString(len: number): string {
  const chars = "abcdefghijklmnopqrstuvwxyz";
  let result = "";
  for (let i = 0; i < len; i++) {
    result += chars[Math.floor(Math.random() * 26)];
  }
  return result;
}

/**
 * Create an anagram of s by shuffling its characters.
 */
function shuffle(s: string): string {
  const arr = s.split("");
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = arr[i]!;
    arr[i] = arr[j]!;
    arr[j] = tmp;
  }
  return arr.join("");
}

interface PerfResult {
  name: string;
  size: number;
  ms: number;
  opsPerSec: number;
}

function benchmark(fn: AnagramFn, s: string, t: string, iterations = 200): number {
  // warm-up
  for (let i = 0; i < 10; i++) fn(s, t);

  const start = performance.now();
  for (let i = 0; i < iterations; i++) {
    fn(s, t);
  }
  const end = performance.now();
  return (end - start) / iterations; // average ms per call
}

describe("Performance analysis", () => {
  const sizes = [100, 1_000, 5_000, 10_000, 20_000];
  const results: PerfResult[] = [];

  for (const size of sizes) {
    const base = randomString(size);
    const anagram = shuffle(base); // true case
    const lastChar = base.at(-1) ?? "a";
    const almost = base.slice(0, -1) + (lastChar === "a" ? "b" : "a"); // false case

    for (const { name, fn } of algorithms) {
      const msTrue = benchmark(fn, base, anagram);
      const msFalse = benchmark(fn, base, almost);
      const avgMs = (msTrue + msFalse) / 2;

      results.push({
        name,
        size,
        ms: avgMs,
        opsPerSec: 1000 / avgMs,
      });
    }
  }

  it("prints performance table", () => {
    console.log("\n=== Valid Anagram – Performance Analysis ===\n");
    console.log(
      "Size".padEnd(8) +
        "Algorithm".padEnd(28) +
        "Avg ms".padStart(10) +
        "Ops/sec".padStart(12)
    );
    console.log("-".repeat(58));

    for (const size of sizes) {
      const row = results.filter((r) => r.size === size);
      for (const r of row) {
        console.log(
          String(r.size).padEnd(8) +
            r.name.padEnd(28) +
            r.ms.toFixed(4).padStart(10) +
            Math.round(r.opsPerSec).toString().padStart(12)
        );
      }
      console.log("-".repeat(58));
    }

    const largest = sizes[sizes.length - 1]!;
    const sortMs = results.find(
      (r) => r.size === largest && r.name.includes("Sort")
    )!.ms;
    const optMs = results.find(
      (r) => r.size === largest && r.name.includes("Optimal")
    )!.ms;
    const speedup = sortMs / optMs;

    console.log(
      `\nSpeed-up (Optimal vs Sort) @ n=${largest}: ${speedup.toFixed(1)}×\n`
    );

    expect(true).toBe(true);
  });

  it("Optimal is faster than Sort for large inputs", () => {
    const largest = sizes[sizes.length - 1]!;
    const sort = results.find(
      (r) => r.size === largest && r.name.includes("Sort")
    )!;
    const optimal = results.find(
      (r) => r.size === largest && r.name.includes("Optimal")
    )!;

    expect(optimal.ms).toBeLessThan(sort.ms);
  });
});