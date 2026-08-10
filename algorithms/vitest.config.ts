import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["algorithms/**/*.test.ts", "fullstack/**/*.test.ts"],
    environment: "node",
    globals: false,

    // Performance profiling
    benchmark: {
      include: ["algorithms/**/*.bench.ts"],
      reporters: ["verbose"],
      outputJson: "reports/benchmarks/vitest-bench.json",
    },

    coverage: {
      provider: "v8",
      reporter: ["text", "html", "json-summary"],
      reportsDirectory: "reports/coverage",
    },

    // Surface slow tests so regressions in algorithmic complexity are
    // visible directly in CI output rather than only in benchmark.ts.
    slowTestThreshold: 200,

    reporters: ["default"],
    outputFile: {
      json: "reports/vitest-results.json",
    },
  },
});
