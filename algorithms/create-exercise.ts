import * as path from "node:path";
import { createExerciseScaffold } from "./exercise-scaffold";

const [, , sourcePathArg] = process.argv;

if (!sourcePathArg) {
  console.error("Usage: ts-node algorithms/create-exercise.ts <category/problem-name>");
  process.exit(1);
}

const repoRoot = process.cwd();
const result = createExerciseScaffold({
  sourcePath: sourcePathArg,
  destinationRoot: path.join(repoRoot, "algorithms"),
});

console.log(`Exercise scaffold created at ${result.destinationPath}`);
console.log(`Copied files: ${result.copiedFiles.join(", ")}`);
