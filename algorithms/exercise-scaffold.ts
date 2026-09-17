import * as fs from "node:fs";
import * as path from "node:path";

export interface ExerciseScaffoldOptions {
  sourcePath: string;
  destinationRoot: string;
  destinationFolderName?: string;
}

export interface ExerciseScaffoldResult {
  destinationPath: string;
  copiedFiles: string[];
}

export function createExerciseScaffold({
  sourcePath,
  destinationRoot,
  destinationFolderName = "exercice",
}: ExerciseScaffoldOptions): ExerciseScaffoldResult {
  const normalizedSource = sourcePath.replace(/\\/g, "/").replace(/^\//, "");
  const sourceAbsolutePath = path.isAbsolute(sourcePath)
    ? sourcePath
    : path.join(destinationRoot, normalizedSource);

  if (!fs.existsSync(sourceAbsolutePath)) {
    throw new Error(`Source exercise path does not exist: ${sourceAbsolutePath}`);
  }

  const destinationPath = path.join(destinationRoot, destinationFolderName, normalizedSource);
  fs.mkdirSync(destinationPath, { recursive: true });

  const copiedFiles: string[] = [];
  const entries = fs.readdirSync(sourceAbsolutePath, { withFileTypes: true });

  for (const entry of entries) {
    const sourceEntryPath = path.join(sourceAbsolutePath, entry.name);
    const destinationEntryPath = path.join(destinationPath, entry.name);

    if (entry.isDirectory()) {
      fs.cpSync(sourceEntryPath, destinationEntryPath, { recursive: true });
      continue;
    }

    fs.copyFileSync(sourceEntryPath, destinationEntryPath);
    copiedFiles.push(entry.name);
  }

  const exerciseDoc = `# Exercise Copy

Source: ${normalizedSource}

## Goal
Create a working copy of the problem scaffold for hands-on practice and verification.

## Suggested Workflow
1. Review the problem statement and constraints.
2. Implement the solution in the copied source files.
3. Run the tests and measure complexity.
4. Document the approach and performance trade-offs.
`;

  fs.writeFileSync(path.join(destinationPath, "exercise.md"), exerciseDoc, "utf8");
  copiedFiles.push("exercise.md");

  return {
    destinationPath,
    copiedFiles,
  };
}
