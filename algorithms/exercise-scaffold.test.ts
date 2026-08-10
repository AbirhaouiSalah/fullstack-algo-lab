import { mkdtempSync, mkdirSync, rmSync, writeFileSync, existsSync } from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { describe, expect, it } from "vitest";
import { createExerciseScaffold } from "./exercise-scaffold";

describe("createExerciseScaffold", () => {
  it("creates a new exercise folder by copying an existing problem scaffold", () => {
    const tempRoot = mkdtempSync(path.join(os.tmpdir(), "exercise-scaffold-"));
    const algorithmsRoot = path.join(tempRoot, "algorithms");
    const sourceDir = path.join(algorithmsRoot, "arrays", "two-sum");

    mkdirSync(sourceDir, { recursive: true });
    writeFileSync(path.join(sourceDir, "README.md"), "# Two Sum\n", "utf8");
    writeFileSync(path.join(sourceDir, "solution.ts"), "export function solve(): void {}\n", "utf8");

    try {
      const result = createExerciseScaffold({
        sourcePath: "arrays/two-sum",
        destinationRoot: algorithmsRoot,
      });

      expect(result.destinationPath).toBe(path.join(algorithmsRoot, "exercice", "arrays", "two-sum"));
      expect(existsSync(path.join(result.destinationPath, "README.md"))).toBe(true);
      expect(existsSync(path.join(result.destinationPath, "solution.ts"))).toBe(true);
      expect(existsSync(path.join(result.destinationPath, "exercise.md"))).toBe(true);
      expect(result.copiedFiles).toContain("README.md");
      expect(result.copiedFiles).toContain("solution.ts");
    } finally {
      rmSync(tempRoot, { recursive: true, force: true });
    }
  });
});
