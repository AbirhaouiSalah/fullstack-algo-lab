import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("valid-palindrome", () => {
  it("returns true for a classic palindrome with punctuation, spaces and mixed case", () => {
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

  it("returns true for a string consisting only of non-alphanumeric characters", () => {
    expect(solve(".,!?   @#$")).toBe(true);
  });

  it("returns true for a numeric palindrome", () => {
    expect(solve("12321")).toBe(true);
  });

  it("returns false for non-palindromic numbers", () => {
    expect(solve("12345")).toBe(false);
  });

  it("returns true for a alphanumeric mixed palindrome", () => {
    expect(solve("0P")).toBe(false);
    expect(solve("A1b21a")).toBe(false);
    expect(solve("A1b2b1a")).toBe(true);
  });

  it("returns true for two identical characters with different case", () => {
    expect(solve("aA")).toBe(true);
  });

  it("returns false for two different characters", () => {
    expect(solve("ab")).toBe(false);
  });
});