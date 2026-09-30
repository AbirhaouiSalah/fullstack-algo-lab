import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { describe, expect, it } from "vitest";
import { collectLearningLabStatus } from "./learning-lab";

describe("collectLearningLabStatus", () => {
  it("reports complete and incomplete problems from the algorithms tree", () => {
    const tempRoot = mkdtempSync(path.join(os.tmpdir(), "learning-lab-"));
    const algorithmsRoot = path.join(tempRoot, "algorithms");
    const completeDir = path.join(algorithmsRoot, "arrays", "two-sum");
    const incompleteDir = path.join(algorithmsRoot, "graphs", "course-schedule");

    mkdirSync(completeDir, { recursive: true });
    mkdirSync(incompleteDir, { recursive: true });

    writeFileSync(path.join(completeDir, "README.md"), "# Two Sum\n", "utf8");
    writeFileSync(path.join(completeDir, "solution.ts"), "export const x = 1;\n", "utf8");
    writeFileSync(path.join(completeDir, "solution.test.ts"), "test\n", "utf8");
    writeFileSync(path.join(completeDir, "complexity.md"), "# Complexity\n", "utf8");

    writeFileSync(path.join(incompleteDir, "README.md"), "# Course Schedule\n", "utf8");
    writeFileSync(path.join(incompleteDir, "solution.ts"), "export const x = 1;\n", "utf8");

    try {
      const status = collectLearningLabStatus(algorithmsRoot);

      expect(status.totalProblems).toBe(2);
      expect(status.completeProblems).toBe(1);
      expect(status.incompleteProblems).toHaveLength(1);
      expect(status.incompleteProblems[0]?.name).toBe("course-schedule");
      expect(status.incompleteProblems[0]?.missingFiles).toContain("solution.test.ts");
      expect(status.incompleteProblems[0]?.missingFiles).toContain("complexity.md");
    } finally {
      rmSync(tempRoot, { recursive: true, force: true });
    }
  });
});
