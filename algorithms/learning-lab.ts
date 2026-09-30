import * as fs from "node:fs";
import * as path from "node:path";

export interface LearningLabProblemStatus {
  category: string;
  name: string;
  complete: boolean;
  missingFiles: string[];
}

export interface LearningLabStatus {
  totalProblems: number;
  completeProblems: number;
  incompleteProblems: LearningLabProblemStatus[];
}

const REQUIRED_FILES = ["README.md", "solution.ts", "solution.test.ts", "complexity.md"] as const;

export function collectLearningLabStatus(algorithmsRoot: string): LearningLabStatus {
  if (!fs.existsSync(algorithmsRoot)) {
    return { totalProblems: 0, completeProblems: 0, incompleteProblems: [] };
  }

  const categories = fs.readdirSync(algorithmsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .filter((name) => !name.startsWith("."));

  const problems: LearningLabProblemStatus[] = [];

  for (const category of categories) {
    const categoryPath = path.join(algorithmsRoot, category);
    const problemFolders = fs.readdirSync(categoryPath, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name);

    for (const name of problemFolders) {
      const problemPath = path.join(categoryPath, name);
      const missingFiles = REQUIRED_FILES.filter((fileName) => !fs.existsSync(path.join(problemPath, fileName)));

      if (missingFiles.length > 0) {
        problems.push({ category, name, complete: false, missingFiles });
      } else {
        problems.push({ category, name, complete: true, missingFiles: [] });
      }
    }
  }

  const completeProblems = problems.filter((problem) => problem.complete);
  const incompleteProblems = problems.filter((problem) => !problem.complete);

  return {
    totalProblems: problems.length,
    completeProblems: completeProblems.length,
    incompleteProblems,
  };
}
