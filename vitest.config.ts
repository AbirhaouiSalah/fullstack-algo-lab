import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["algorithms/**/*.test.ts", "fullstack/**/*.test.ts"],
    environment: "node",
    globals: false,
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
    },
  },
});
