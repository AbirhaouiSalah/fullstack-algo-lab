import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("valid-palindrome", () => {
  it("returns true for a palindrome with punctuation and mixed case", () => {
    expect(solve("A man, a plan, a canal: Panama")).toBe(true);
  });

  it("returns false for a non-palindrome", () => {
    expect(solve("race a car")).toBe(false);
  });

  it("returns true for an empty string", () => {
    expect(solve("")).toBe(true);
  });

  it("returns true for a single character", () => {
    expect(solve("a")).toBe(true);
  });

  it("returns true when the string has no alphanumeric characters", () => {
    expect(solve(".,!?")).toBe(true);
  });

  it("returns true for numeric palindromes", () => {
    expect(solve("12321")).toBe(true);
  });
});
