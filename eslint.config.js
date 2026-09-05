import tsParser from "@typescript-eslint/parser";

export default [
  {
    files: ["**/*.{js,ts}"],
    ignores: ["node_modules/**", "**/.venv/**"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
      },
    },
    rules: {},
  },
];