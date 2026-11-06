import { performance } from "node:perf_hooks";

export interface BenchmarkResult {
  inputSize: number;
  executionTimeMs: number;
  memoryAllocatedMB: number;
}

/**
 * Executes a function under performance and memory monitoring.
 */
export function benchmarkAlgorithm<T>(
  fn: (input: T) => unknown,
  inputGenerator: (size: number) => T,
  sizes: number[] = [100, 10000, 1000000]
): BenchmarkResult[] {
  const results: BenchmarkResult[] = [];

  for (const size of sizes) {
    const input = inputGenerator(size);

    // Trigger Garbage Collector if exposed in Node environment
    if (global.gc) {
      global.gc();
    }

    const startMemory = process.memoryUsage().heapUsed;
    const startTime = performance.now();

    fn(input);

    const endTime = performance.now();
    const endMemory = process.memoryUsage().heapUsed;

    const timeSpent = Number((endTime - startTime).toFixed(4));
    const memoryUsed = Number(
      (Math.max(0, endMemory - startMemory) / 1024 / 1024).toFixed(4)
    );

    results.push({
      inputSize: size,
      executionTimeMs: timeSpent,
      memoryAllocatedMB: memoryUsed,
    });
  }

  return results;
}