import * as fs from "node:fs";
import * as path from "node:path";

interface ProblemMeta {
  category: string;
  name: string;
  hasSolution: boolean;
  hasTests: boolean;
  hasComplexityDoc: boolean;
}

const ALGO_DIR = path.join(process.cwd(), "algorithms");
const REPORT_FILE = path.join(process.cwd(), "docs", "algorithms", "progress.md");

function getProblemStatus(): ProblemMeta[] {
  if (!fs.existsSync(ALGO_DIR)) return [];

  const categories = fs.readdirSync(ALGO_DIR);
  const problems: ProblemMeta[] = [];

  for (const category of categories) {
    const categoryPath = path.join(ALGO_DIR, category);
    if (!fs.statSync(categoryPath).isDirectory()) continue;

    const problemFolders = fs.readdirSync(categoryPath);
    for (const name of problemFolders) {
      const probPath = path.join(categoryPath, name);
      if (!fs.statSync(probPath).isDirectory()) continue;

      problems.push({
        category,
        name,
        hasSolution: fs.existsSync(path.join(probPath, "solution.ts")),
        hasTests: fs.existsSync(path.join(probPath, "solution.test.ts")),
        hasComplexityDoc: fs.existsSync(path.join(probPath, "complexity.md")),
      });
    }
  }

  return problems;
}

function generateMarkdownReport(): void {
  const problems = getProblemStatus();
  const total = problems.length;
  const completed = problems.filter(
    (p) => p.hasSolution && p.hasTests && p.hasComplexityDoc
  ).length;

  let md = `# Algorithm Laboratory Progress Report\n\n`;
  md += `**Overall Completion:** ${completed} / ${total} Problems Validated\n\n`;
  md += `| Category | Problem | Solution (\.ts) | Test Suite (\.test.ts) | Complexity Doc (\.md) | Status |\n`;
  md += `| :--- | :--- | :---: | :---: | :---: | :---: |\n`;

  for (const p of problems) {
    const isComplete = p.hasSolution && p.hasTests && p.hasComplexityDoc;
    const status = isComplete ? "✅ Mastered" : "🚧 In Progress";
    md += `| \`${p.category}\` | \`${p.name}\` | ${p.hasSolution ? "✔" : "❌"} | ${p.hasTests ? "✔" : "❌"} | ${p.hasComplexityDoc ? "✔" : "❌"} | ${status} |\n`;
  }

  fs.mkdirSync(path.dirname(REPORT_FILE), { recursive: true });
  fs.writeFileSync(REPORT_FILE, md, "utf-8");
  console.log(`Progress report successfully written to ${REPORT_FILE}`);
}

generateMarkdownReport();